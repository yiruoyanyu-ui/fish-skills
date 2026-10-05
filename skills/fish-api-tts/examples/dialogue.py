"""多说话人对话（需 S2 家族模型，如 s2-pro）。
用法: python dialogue.py <speaker0_音色id> <speaker1_音色id> [out.mp3]
说话人下标对应 reference_id 数组位置，文本里用 <|speaker:N|> 切换。"""
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
