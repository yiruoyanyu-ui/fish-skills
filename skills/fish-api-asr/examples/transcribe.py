"""REST transcription with timestamps and speaker turns. Usage: python transcribe.py audio.mp3 [language] [model]. Send ignore_timestamps=false; select the model in the HTTP header."""
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
        timeout=900,  # Long audio may take several minutes
    )
if r.status_code != 200:
    sys.exit(f"HTTP {r.status_code}: {r.text[:300]}")
result = r.json()
if not result.get("segments"):
    sys.exit("Empty segments: check ignore_timestamps=false and that audio contains speech")
print(f"OK model {model}, duration  {result['duration']:.2f}s, language  {result.get('language_code')}，"
      f"{len(result['segments'])} segments, {len(result.get('speaker_turns', []))} speaker turns")
print(result["text"])
for t in result.get("speaker_turns", []):
    print(f"  {t['speaker']} [{t['start']:.2f}-{t['end']:.2f}] {t['text']}")
print(json.dumps(result["segments"][:5], ensure_ascii=False))
