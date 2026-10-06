"""Synchronous voice design. Usage: python design.py "description" [audition text] [n]. Saves candidate WAV files and prints candidate metadata."""
import base64
import os
import sys

import requests

instruction = sys.argv[1]
reference_text = sys.argv[2] if len(sys.argv) > 2 else ""
n = int(sys.argv[3]) if len(sys.argv) > 3 else 1

body = {"instruction": instruction, "n": n}
if reference_text:
    body["reference_text"] = reference_text

r = requests.post(
    "https://api.fish.audio/v1/voice-design",
    headers={
        "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
        "Content-Type": "application/json",
    },
    json=body,
    timeout=180,
)
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
for c in r.json()["candidates"]:
    wav = base64.b64decode(c["audio_base64"])
    path = f"candidate_{c['index']}.wav"
    with open(path, "wb") as f:
        f.write(wav)
    print(path, f"{c['duration_ms']}ms {c['sample_rate']}Hz", "|", c["features"].get("description"))
