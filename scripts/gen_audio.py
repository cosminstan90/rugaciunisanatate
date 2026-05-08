#!/usr/bin/env python3
"""
ElevenLabs TTS generator for rugaciunisanatate.ro prayers.

Usage:
  python scripts/gen_audio.py --list           # See prayers without audio
  python scripts/gen_audio.py --dry-run        # Count chars, estimate quota usage
  python scripts/gen_audio.py --limit 5        # Generate audio for 5 prayers
  python scripts/gen_audio.py --slug rugaciune-de-dimineata  # Single prayer
  python scripts/gen_audio.py --limit 5 --voice female  # Use female voice

Requirements:
  pip install requests psycopg2-binary python-dotenv

Environment variables (in .env or shell):
  ELEVENLABS_API_KEY=sk_...
  DATABASE_URL=postgresql://ruguser:PASSWORD@localhost:5432/rugaciunisanatate
  AUDIO_OUTPUT_DIR=public/audio   (optional, default: public/audio)
"""

import argparse
import json
import os
import re
import sys
import time
import requests

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    print("ERROR: pip install psycopg2-binary")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://ruguser:2awOYwfEZa5Evgi8KUb2@localhost:5432/rugaciunisanatate"
)

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")

# ElevenLabs voice IDs - Romanian-compatible
VOICES = {
    # Male: deep, calm, suitable for orthodox prayers
    "male": "pNInz6obpgDQGcFmaJgB",    # Adam - neutral, works well with Romanian
    # Female: warm, devotional tone
    "female": "EXAVITQu4vr4xnSDxMaL",  # Bella - warm female voice
    # Romanian-specific (if you have access on paid plan)
    # "male_ro": "YOUR_CLONED_VOICE_ID",
}

MODEL = "eleven_multilingual_v2"  # Supports Romanian natively

AUDIO_DIR = os.environ.get("AUDIO_OUTPUT_DIR", "public/audio")

# ElevenLabs API
TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
INFO_URL = "https://api.elevenlabs.io/v1/user/subscription"

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def pt_to_text(value) -> str:
    """Convert PortableText (list of blocks) or plain string to plain text."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts = []
        for block in value:
            if not isinstance(block, dict):
                continue
            if block.get("_type") == "block":
                children = block.get("children", [])
                text = "".join(
                    child.get("text", "") for child in children
                    if isinstance(child, dict)
                )
                if text.strip():
                    parts.append(text.strip())
        return "\n\n".join(parts)
    return str(value)


def get_db():
    return psycopg2.connect(DB_URL)


def fetch_prayers_without_audio(conn, limit: int = 999, slug: str = None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        if slug:
            cur.execute(
                "SELECT id, slug, title, content, category FROM ec_rugaciuni "
                "WHERE status = 'published' AND slug = %s",
                (slug,)
            )
        else:
            cur.execute(
                "SELECT id, slug, title, content, category FROM ec_rugaciuni "
                "WHERE status = 'published' AND (audio_url IS NULL OR audio_url = '') "
                "ORDER BY published_at DESC LIMIT %s",
                (limit,)
            )
        return cur.fetchall()


def update_audio_url(conn, slug: str, url: str):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE ec_rugaciuni SET audio_url = %s WHERE slug = %s",
            (url, slug)
        )
    conn.commit()


def check_quota(api_key: str) -> dict:
    """Check remaining ElevenLabs character quota."""
    r = requests.get(INFO_URL, headers={"xi-api-key": api_key}, timeout=10)
    if r.status_code != 200:
        return {"error": r.text}
    data = r.json()
    used = data.get("character_count", 0)
    limit = data.get("character_limit", 10000)
    return {
        "used": used,
        "limit": limit,
        "remaining": limit - used,
        "plan": data.get("tier", "free"),
    }


def generate_audio(text: str, voice_id: str, api_key: str) -> bytes:
    """Call ElevenLabs TTS API and return MP3 bytes."""
    url = TTS_URL.format(voice_id=voice_id)
    payload = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.80,
            "style": 0.05,
            "use_speaker_boost": True,
        },
    }
    r = requests.post(
        url,
        json=payload,
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        timeout=120,
    )
    if r.status_code != 200:
        raise RuntimeError(f"ElevenLabs API error {r.status_code}: {r.text[:300]}")
    return r.content


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[ăâ]", "a", text)
    text = re.sub(r"[îi]", "i", text)
    text = re.sub(r"[șş]", "s", text)
    text = re.sub(r"[țţ]", "t", text)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


# ─── COMMANDS ──────────────────────────────────────────────────────────────────

def cmd_list(conn):
    rows = fetch_prayers_without_audio(conn)
    if not rows:
        print("✅ All published prayers already have audio!")
        return
    total_chars = 0
    print(f"{'SLUG':<50} {'CHARS':>6}  TITLE")
    print("-" * 80)
    for row in rows:
        text = pt_to_text(row["content"])
        chars = len(text)
        total_chars += chars
        title = pt_to_text(row["title"])[:40]
        print(f"{row['slug']:<50} {chars:>6}  {title}")
    print("-" * 80)
    print(f"Total: {len(rows)} prayers, {total_chars:,} characters")
    print(f"ElevenLabs free tier: 10,000 chars/month")
    print(f"Prayers processable on free tier: ~{10000 // (total_chars // max(len(rows), 1))}")


def cmd_dry_run(conn, limit: int, voice: str):
    rows = fetch_prayers_without_audio(conn, limit)
    total_chars = sum(len(pt_to_text(r["content"])) for r in rows)
    print(f"DRY RUN — would process {len(rows)} prayers")
    print(f"Total characters: {total_chars:,}")
    print(f"Voice: {voice} ({VOICES[voice]})")
    print(f"Model: {MODEL}")
    print()
    if API_KEY:
        quota = check_quota(API_KEY)
        if "error" not in quota:
            print(f"Quota: {quota['used']:,} used / {quota['limit']:,} limit ({quota['remaining']:,} remaining)")
            if total_chars > quota["remaining"]:
                print(f"⚠️  NOT ENOUGH QUOTA — need {total_chars:,}, have {quota['remaining']:,}")
            else:
                print(f"✅ Quota OK — {quota['remaining'] - total_chars:,} chars left after processing")
    else:
        print("⚠️  No ELEVENLABS_API_KEY set — quota check skipped")


def cmd_generate(conn, limit: int, voice: str, slug: str = None, dry_run: bool = False):
    if not API_KEY:
        print("ERROR: Set ELEVENLABS_API_KEY environment variable")
        sys.exit(1)

    voice_id = VOICES.get(voice, VOICES["male"])
    rows = fetch_prayers_without_audio(conn, limit, slug)

    if not rows:
        print("No prayers to process (all have audio or slug not found)")
        return

    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Check quota first
    quota = check_quota(API_KEY)
    if "error" in quota:
        print(f"⚠️  Could not check quota: {quota['error']}")
    else:
        total_chars = sum(len(pt_to_text(r["content"])) for r in rows)
        print(f"Quota: {quota['remaining']:,} chars remaining | Need: {total_chars:,} chars")
        if total_chars > quota["remaining"]:
            print(f"❌ Not enough quota! Reduce --limit or wait for monthly reset.")
            sys.exit(1)

    print(f"\nGenerating audio for {len(rows)} prayers using voice '{voice}'...\n")

    for i, row in enumerate(rows, 1):
        prayer_slug = row["slug"]
        title = pt_to_text(row["title"])
        content = pt_to_text(row["content"])

        if not content.strip():
            print(f"[{i}/{len(rows)}] ⚠️  SKIP {prayer_slug} — no content")
            continue

        filename = f"{prayer_slug}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        audio_url = f"/audio/{filename}"

        chars = len(content)
        print(f"[{i}/{len(rows)}] {prayer_slug}")
        print(f"         Title:  {title[:60]}")
        print(f"         Chars:  {chars:,}")

        if os.path.exists(filepath):
            print(f"         File:   already exists → skipping API call, updating DB")
            update_audio_url(conn, prayer_slug, audio_url)
            print(f"         DB:     ✅ updated")
            continue

        try:
            audio_bytes = generate_audio(content, voice_id, API_KEY)
            with open(filepath, "wb") as f:
                f.write(audio_bytes)
            print(f"         File:   ✅ saved ({len(audio_bytes):,} bytes)")

            update_audio_url(conn, prayer_slug, audio_url)
            print(f"         DB:     ✅ updated audio_url = {audio_url}")

        except Exception as e:
            print(f"         ❌ ERROR: {e}")
            continue

        # Small delay to avoid rate limiting
        if i < len(rows):
            time.sleep(1.5)

    print(f"\nDone! Audio files saved to {AUDIO_DIR}/")
    print("Run: git add public/audio/ && git commit -m 'Add prayer audio files' && git push")
    print("Then on server: git pull && pm2 restart rugaciunisanatate")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ElevenLabs TTS for rugaciunisanatate.ro")
    parser.add_argument("--list", action="store_true", help="List prayers without audio")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be processed")
    parser.add_argument("--limit", type=int, default=5, help="Max prayers to process (default: 5)")
    parser.add_argument("--slug", type=str, help="Process a single prayer by slug")
    parser.add_argument("--voice", choices=["male", "female"], default="male", help="Voice to use")
    args = parser.parse_args()

    conn = get_db()
    try:
        if args.list:
            cmd_list(conn)
        elif args.dry_run:
            cmd_dry_run(conn, args.limit, args.voice)
        else:
            cmd_generate(conn, args.limit, args.voice, args.slug)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
