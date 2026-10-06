"""SSE TTS with timestamps. Usage: python sse_timestamps.py "text" [reference_id]. Outputs out.mp3 and timings.json; times are seconds."""
import base64
import json
import os
import sys

import requests

text = sys.argv[1]
reference_id = sys.argv[2] if len(sys.argv) > 2 else ""
body = {"text": text, "format": "mp3"}
if reference_id:
    body["reference_id"] = reference_id

audio = bytearray()
# chunk_seq -> (chunk_audio_offset_sec, segments)。Alignment is cumulative per chunk: replace the previous snapshot, do not append
snapshots = {}

with requests.post(
    "https://api.fish.audio/v1/tts/stream/with-timestamp",
    headers={
        "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
        "Content-Type": "application/json",
        "model": "s2-pro",
    },
    json=body,
    stream=True,
    timeout=120,
) as r:
    if r.status_code != 200:
        sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
    r.encoding = "utf-8"  # Decode SSE as UTF-8 rather than requests default ISO-8859-1
    for line in r.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        event = json.loads(line[5:].strip())
        if event.get("audio_base64"):
            audio += base64.b64decode(event["audio_base64"])
        alignment = event.get("alignment")
        if alignment:
            snapshots[event["chunk_seq"]] = (
                event["chunk_audio_offset_sec"],
                alignment["segments"],
            )

timings = []
for seq in sorted(snapshots):
    offset, segments = snapshots[seq]
    for s in segments:
        timings.append(
            {
                "text": s["text"],
                "start": round(offset + s["start"], 3),
                "end": round(offset + s["end"], 3),
            }
        )

with open("out.mp3", "wb") as f:
    f.write(audio)
with open("timings.json", "w", encoding="utf-8") as f:
    json.dump(timings, f, ensure_ascii=False, indent=1)
print(f"OK audio {len(audio)} bytes，{len(timings)} character/word timings -> out.mp3 / timings.json")
