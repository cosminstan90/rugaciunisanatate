#!/usr/bin/env python3
"""
Generate AI images for Orthodox saints using OpenAI DALL-E 3.
Saves images to public/sfinti/ and updates photo_url in ec_sfinti.

Usage:
  pip install openai psycopg2-binary requests python-dotenv

  OPENAI_API_KEY=sk-... python scripts/gen_saint_images.py --list
  OPENAI_API_KEY=sk-... python scripts/gen_saint_images.py --dry-run
  OPENAI_API_KEY=sk-... python scripts/gen_saint_images.py --all
  OPENAI_API_KEY=sk-... python scripts/gen_saint_images.py --slug sfantul-pantelimon

Cost: ~$0.04/image (DALL-E 3, 1024x1024, standard quality)
      6 saints = ~$0.24 total
"""

import argparse
import os
import sys
import time
import requests

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: pip install openai")
    sys.exit(1)

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
    pass

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://ruguser:2awOYwfEZa5Evgi8KUb2@localhost:5432/rugaciunisanatate"
)
API_KEY = os.environ.get("OPENAI_API_KEY", "")
OUTPUT_DIR = "public/sfinti"

# ─── SAINT PROMPTS ─────────────────────────────────────────────────────────────

# Byzantine icon style — works well with DALL-E 3
BASE_STYLE = (
    "Byzantine Orthodox icon painting style, gold leaf background, flat medieval iconographic art, "
    "rich warm colors, halos depicted as golden circles, traditional Orthodox iconography, "
    "formal frontal composition, egg tempera on wood panel aesthetic, "
    "no photography, no modern elements, icon-like quality"
)

SAINTS = {
    "sfantul-pantelimon": {
        "name": "Sfântul Pantelimon",
        "prompt": (
            f"Orthodox icon of Saint Panteleimon the Healer and Great Martyr, "
            f"young man with short dark hair and golden halo, wearing red martyrs robe over white tunic, "
            f"holding a small medical box and a spoon in his hands, gentle compassionate expression, "
            f"Byzantine mosaic gold background. {BASE_STYLE}. Square format 1:1."
        ),
    },
    "sfantul-nectarie": {
        "name": "Sfântul Nectarie",
        "prompt": (
            f"Orthodox icon of Saint Nectarios of Aegina, "
            f"elderly bishop with white beard, wearing dark episcopal vestments and white omophorion with crosses, "
            f"golden episcopal crown, holding a Gospel book, kind gentle expression with golden halo, "
            f"Byzantine gold background. {BASE_STYLE}. Square format 1:1."
        ),
    },
    "sfantul-luca-al-crimeei": {
        "name": "Sfântul Luca al Crimeei",
        "prompt": (
            f"Orthodox icon of Saint Luke of Crimea, Archbishop and surgeon, "
            f"elderly bishop with white beard wearing episcopal vestments, holding scalpel in one hand and Gospel in the other, "
            f"large golden halo, spectacles, warm compassionate expression, "
            f"deep blue episcopal robe, Byzantine gold background. {BASE_STYLE}. Square format 1:1."
        ),
    },
    "sfantul-mina": {
        "name": "Sfântul Mina",
        "prompt": (
            f"Orthodox icon of Saint Menas the Great Martyr of Egypt, "
            f"young Roman soldier wearing red military cloak over armor, "
            f"holding martyr cross and shield, golden halo, determined noble expression, "
            f"standing frontally in traditional iconographic pose, "
            f"Byzantine gold background. {BASE_STYLE}. Square format 1:1."
        ),
    },
    "cosma-si-damian": {
        "name": "Sfinții Cosma și Damian",
        "prompt": (
            f"Orthodox icon of the Holy Unmercenary Physicians Saints Cosmas and Damian, "
            f"two identical twin brothers standing together, both with golden halos, "
            f"wearing Byzantine physician robes, each holding a small medical box of herbs, "
            f"young gentle faces, formal symmetrical composition, "
            f"Byzantine gold background. {BASE_STYLE}. Square format 1:1."
        ),
    },
    "sfanta-parascheva": {
        "name": "Sfânta Parascheva",
        "prompt": (
            f"Orthodox icon of Saint Paraskeva the New of Iași, "
            f"young woman ascetic saint with golden halo, wearing simple dark monastic robe and white head covering, "
            f"holding a small cross, gentle peaceful expression, "
            f"formal frontal Byzantine composition, gold background with subtle decorative border. "
            f"{BASE_STYLE}. Square format 1:1."
        ),
    },
}

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def get_db():
    return psycopg2.connect(DB_URL)


def fetch_saints(conn, slug=None):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        if slug:
            cur.execute(
                "SELECT slug, name, photo_url FROM ec_sfinti WHERE status='published' AND slug=%s",
                (slug,)
            )
        else:
            cur.execute(
                "SELECT slug, name, photo_url FROM ec_sfinti WHERE status='published' ORDER BY slug"
            )
        return cur.fetchall()


def update_photo_url(conn, slug: str, url: str):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE ec_sfinti SET photo_url=%s WHERE slug=%s",
            (url, slug)
        )
    conn.commit()


def download_image(url: str, filepath: str):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    with open(filepath, "wb") as f:
        f.write(r.content)
    return len(r.content)


# ─── COMMANDS ──────────────────────────────────────────────────────────────────

def cmd_list(conn):
    rows = fetch_saints(conn)
    print(f"{'SLUG':<35} {'PHOTO_URL':<30} PROMPT?")
    print("-" * 75)
    for row in rows:
        has_prompt = "✅" if row["slug"] in SAINTS else "❌ no prompt"
        has_photo = row["photo_url"] or "—"
        print(f"{row['slug']:<35} {has_photo:<30} {has_prompt}")
    print(f"\n{len(rows)} saints total. Cost estimate: ${len(SAINTS) * 0.04:.2f} for all.")


def cmd_dry_run():
    print("DRY RUN — prompts that would be sent to DALL-E 3:\n")
    for slug, info in SAINTS.items():
        print(f"[{info['name']}]")
        print(f"  File: public/sfinti/{slug}.png")
        print(f"  Prompt ({len(info['prompt'])} chars):")
        print(f"  {info['prompt'][:120]}...")
        print()
    print(f"Total: {len(SAINTS)} images × $0.04 = ${len(SAINTS) * 0.04:.2f}")
    print("Model: dall-e-3, size: 1024x1024, quality: standard")


def cmd_generate(conn, slug=None):
    if not API_KEY:
        print("ERROR: Set OPENAI_API_KEY environment variable")
        sys.exit(1)

    client = OpenAI(api_key=API_KEY)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if slug:
        if slug not in SAINTS:
            print(f"ERROR: No prompt defined for '{slug}'. Available: {list(SAINTS.keys())}")
            sys.exit(1)
        targets = {slug: SAINTS[slug]}
    else:
        targets = SAINTS

    print(f"Generating {len(targets)} saint image(s) via DALL-E 3...\n")

    for i, (saint_slug, info) in enumerate(targets.items(), 1):
        filepath = os.path.join(OUTPUT_DIR, f"{saint_slug}.png")
        photo_url = f"/sfinti/{saint_slug}.png"

        print(f"[{i}/{len(targets)}] {info['name']}")

        if os.path.exists(filepath):
            print(f"         File already exists → updating DB only")
            update_photo_url(conn, saint_slug, photo_url)
            print(f"         ✅ DB updated: {photo_url}")
            continue

        try:
            print(f"         Calling DALL-E 3...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=info["prompt"],
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt

            print(f"         Downloading...")
            size_bytes = download_image(image_url, filepath)
            print(f"         ✅ Saved {filepath} ({size_bytes // 1024} KB)")

            update_photo_url(conn, saint_slug, photo_url)
            print(f"         ✅ DB updated: {photo_url}")

            if revised_prompt and revised_prompt != info["prompt"]:
                print(f"         ℹ  DALL-E revised prompt (saved for review)")
                with open(f"scripts/revised_prompt_{saint_slug}.txt", "w", encoding="utf-8") as f:
                    f.write(f"Original:\n{info['prompt']}\n\nRevised:\n{revised_prompt}\n")

        except Exception as e:
            print(f"         ❌ ERROR: {e}")
            continue

        # Delay between requests to avoid rate limits
        if i < len(targets):
            print(f"         Waiting 3s...")
            time.sleep(3)

    print(f"\n✅ Done!")
    print(f"Next steps:")
    print(f"  git add public/sfinti/ && git commit -m 'Add AI-generated saint images' && git push")
    print(f"  On server: git pull && npm run build && pm2 restart rugaciunisanatate")


# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate saint images with DALL-E 3")
    parser.add_argument("--list", action="store_true", help="List saints and their current photo_url")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts without calling API")
    parser.add_argument("--all", action="store_true", help="Generate all 6 saint images")
    parser.add_argument("--slug", type=str, help="Generate image for a single saint by slug")
    args = parser.parse_args()

    if not any([args.list, args.dry_run, args.all, args.slug]):
        parser.print_help()
        sys.exit(1)

    if args.dry_run:
        cmd_dry_run()
        return

    conn = get_db()
    try:
        if args.list:
            cmd_list(conn)
        elif args.all or args.slug:
            cmd_generate(conn, args.slug)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
