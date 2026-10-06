"""Basic REST TTS. Usage: python basic_tts.py "text" [reference_id] [out.mp3]. An empty voice ID selects the default voice."""
import os
import sys

import requests

text = sys.argv[1] if len(sys.argv) > 1 else "你好，欢迎使用 Fish Audio。"
reference_id = sys.argv[2] if len(sys.argv) > 2 else ""
out = sys.argv[3] if len(sys.argv) > 3 else "out.mp3"

body = {"text": text, "format": "mp3"}
if reference_id:
    body["reference_id"] = reference_id

r = requests.post(
    "https://api.fish.audio/v1/tts",
    headers={
        "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
        "Content-Type": "application/json",
        "model": "s2-pro",
    },
    json=body,
    timeout=120,
)
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
with open(out, "wb") as f:
    f.write(r.content)
print(f"OK {len(r.content)} bytes -> {out}")
