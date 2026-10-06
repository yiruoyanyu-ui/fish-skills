"""Reference-audio TTS using MessagePack. Requires msgpack. Usage: python zero_shot_clone.py ref_audio.mp3 "reference transcript" "new text" [out.mp3]."""
import os
import sys

import msgpack
import requests

ref_path, ref_text, text = sys.argv[1], sys.argv[2], sys.argv[3]
out = sys.argv[4] if len(sys.argv) > 4 else "zero_shot.mp3"

with open(ref_path, "rb") as f:
    reference_audio = f.read()

body = msgpack.packb(
    {
        "text": text,
        "format": "mp3",
        "references": [{"audio": reference_audio, "text": ref_text}],
    },
    use_bin_type=True,  # Encode audio as MessagePack binary
)
r = requests.post(
    "https://api.fish.audio/v1/tts",
    headers={
        "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
        "Content-Type": "application/msgpack",
        "model": "s2-pro",
    },
    data=body,
    timeout=120,
)
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
with open(out, "wb") as f:
    f.write(r.content)
print(f"OK {len(r.content)} bytes -> {out}")
