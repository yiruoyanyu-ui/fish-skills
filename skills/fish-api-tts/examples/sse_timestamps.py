"""流式合成 + 字/词级时间戳（SSE）。
用法: python sse_timestamps.py "文本" [reference_id]
产出: out.mp3（音频）和 timings.json（每个字/词的绝对起止时间，秒）。"""
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
# chunk_seq -> (chunk_audio_offset_sec, segments)。同一 chunk 的 alignment 是累计快照：后到的覆盖先到的，不要追加
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
    r.encoding = "utf-8"  # requests 对 text/event-stream 默认按 ISO-8859-1 解码，中文会乱码
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
print(f"OK 音频 {len(audio)} 字节，{len(timings)} 个字/词时间戳 -> out.mp3 / timings.json")
