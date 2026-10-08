"""Multi-speaker TTS for a supported model. Usage: python dialogue.py <voice0> <voice1> [out.mp3]. Speaker markers index the reference_id array."""
import os
import sys

import requests

v0, v1 = sys.argv[1], sys.argv[2]
out = sys.argv[3] if len(sys.argv) > 3 else "dialogue.mp3"
text = "<|speaker:0|>早上好！<|speaker:1|>早上好，你好吗？<|speaker:0|>很好，谢谢！"

r = requests.post(
    "https://api.fish.audio/v1/tts",
    headers={
        "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
        "Content-Type": "application/json",
        "model": "s2-pro",
    },
    json={"text": text, "reference_id": [v0, v1], "format": "mp3"},
    timeout=120,
)
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
with open(out, "wb") as f:
    f.write(r.content)
print(f"OK {len(r.content)} bytes -> {out}")
