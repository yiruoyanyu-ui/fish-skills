"""Live TTS with MessagePack WebSocket frames. Requires websockets and msgpack. Usage: python ws_live.py "part1" "part2" [--ref ID]. Outputs ws_out.mp3 and ws_timings.json."""
import argparse
import asyncio
import json
import os
import sys

import msgpack
import websockets

parser = argparse.ArgumentParser()
parser.add_argument("fragments", nargs="+")
parser.add_argument("--ref", default="")
args = parser.parse_args()


def pack(obj):
    return msgpack.packb(obj, use_bin_type=True)


async def main():
    request = {"text": "", "format": "mp3", "latency": "balanced", "chunk_length": 100}
    if args.ref:
        request["reference_id"] = args.ref
    audio = bytearray()
    snapshots = {}
    finish = None
    async with websockets.connect(
        "wss://api.fish.audio/v1/tts/live/with-timestamp",
        additional_headers={
            "Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
            "model": "s2-pro",
        },
        max_size=None,
        open_timeout=30,
    ) as ws:
        await ws.send(pack({"event": "start", "request": request}))
        for fragment in args.fragments:
            await ws.send(pack({"event": "text", "text": fragment}))
        await ws.send(pack({"event": "flush"}))
        await ws.send(pack({"event": "stop"}))
        async for raw in ws:
            event = msgpack.unpackb(raw, raw=False)
            kind = event.get("event")
            if kind == "audio":
                audio.extend(event.get("audio") or b"")
                if event.get("alignment"):  # null means no new snapshot for this chunk
                    snapshots[event["chunk_seq"]] = (
                        event["chunk_audio_offset_sec"],
                        event["alignment"]["segments"],
                    )
            elif kind == "finish":
                finish = event
                break
            elif kind == "error":
                sys.exit(f"error: {event}")
    if not finish or finish.get("reason") != "stop":
        sys.exit(f"Unexpected finish: {finish}")
    timings = [
        {"text": s["text"], "start": round(off + s["start"], 3), "end": round(off + s["end"], 3)}
        for _, (off, segs) in sorted(snapshots.items())
        for s in segs
    ]
    with open("ws_out.mp3", "wb") as f:
        f.write(audio)
    with open("ws_timings.json", "w", encoding="utf-8") as f:
        json.dump(timings, f, ensure_ascii=False, indent=1)
    print(f"OK audio {len(audio)} bytes，{len(timings)} character/word timings -> ws_out.mp3 / ws_timings.json")


asyncio.run(main())
