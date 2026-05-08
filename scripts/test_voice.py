#!/usr/bin/env python3
"""
Quick A/B voice test for ElevenLabs.
Generates two short MP3 samples (male + female) from a hardcoded prayer fragment.

Usage:
  ELEVENLABS_API_KEY=sk_xxx python scripts/test_voice.py

Outputs: scripts/test_male.mp3 and scripts/test_female.mp3
"""

import os
import sys
import requests

API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
if not API_KEY:
    print("ERROR: set ELEVENLABS_API_KEY environment variable")
    sys.exit(1)

VOICES = {
    "male":   "pNInz6obpgDQGcFmaJgB",  # Adam
    "female": "EXAVITQu4vr4xnSDxMaL",  # Bella
}

MODEL = "eleven_multilingual_v2"

# First paragraph of a sample prayer
SAMPLE = (
    "Doamne Iisuse Hristoase, Fiul lui Dumnezeu, "
    "miluiește-mă pe mine, păcătosul. "
    "Vindecă sufletul și trupul meu de toată boala și neputința. "
    "Dă-mi sănătate și putere să Te slujesc cu credință până la sfârșitul vieții mele. Amin."
)

def generate(voice_name: str, voice_id: str, text: str) -> str:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    r = requests.post(
        url,
        json={
            "text": text,
            "model_id": MODEL,
            "voice_settings": {
                "stability": 0.55,
                "similarity_boost": 0.80,
                "style": 0.05,
                "use_speaker_boost": True,
            },
        },
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        },
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"{r.status_code}: {r.text[:200]}")
    out = f"scripts/test_{voice_name}.mp3"
    with open(out, "wb") as f:
        f.write(r.content)
    print(f"✅ {voice_name}: saved {out} ({len(r.content):,} bytes)")
    return out

print(f"Sample text ({len(SAMPLE)} chars):\n{SAMPLE}\n")
for name, vid in VOICES.items():
    try:
        generate(name, vid, SAMPLE)
    except Exception as e:
        print(f"❌ {name}: {e}")

print("\nListen to both files and decide which voice to use.")
print("Then run: python scripts/gen_audio.py --limit 5 --voice [male|female]")
