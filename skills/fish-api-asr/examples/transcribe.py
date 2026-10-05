"""语音转文字（REST ASR），带逐字/词时间戳与说话人分段。
用法: python transcribe.py audio.mp3 [language] [model]
  model 默认 transcribe-1-pro（推荐；头缺失会静默按 transcribe-1 处理，长音频会 503）。
注意 ignore_timestamps 默认是 true（segments 为空数组），要时间戳必须显式传 false。"""
import json
import os
import sys

import requests

path = sys.argv[1]
language = sys.argv[2] if len(sys.argv) > 2 else ""
model = sys.argv[3] if len(sys.argv) > 3 else "transcribe-1-pro"
form = {"ignore_timestamps": "false"}
if language:
    form["language"] = language

with open(path, "rb") as f:
    r = requests.post(
        "https://api.fish.audio/v1/asr",
        headers={"Authorization": f"Bearer {os.environ['FISH_API_KEY']}", "model": model},
        files={"audio": f},
        data=form,
        timeout=900,  # 长音频 pro 可能要几分钟
    )
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
result = r.json()
if not result.get("segments"):
    sys.exit("segments 为空：确认 ignore_timestamps=false，且音频里确有人声")
print(f"OK 模型 {model}，时长 {result['duration']:.2f}s，语言 {result.get('language_code')}，"
      f"{len(result['segments'])} 段，{len(result.get('speaker_turns', []))} 个说话人分段")
print(result["text"])
for t in result.get("speaker_turns", []):
    print(f"  {t['speaker']} [{t['start']:.2f}-{t['end']:.2f}] {t['text']}")
print(json.dumps(result["segments"][:5], ensure_ascii=False))
