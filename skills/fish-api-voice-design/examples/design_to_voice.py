"""Design, persist, synthesize and clean up a test voice. Usage: python design_to_voice.py "description" "audition text" [--keep]. Persistence uses the public POST /model endpoint."""
import base64
import os
import sys

import requests

BASE = "https://api.fish.audio"
HEADERS = {"Authorization": f"Bearer {os.environ['FISH_API_KEY']}"}
instruction, reference_text = sys.argv[1], sys.argv[2]
keep = "--keep" in sys.argv

r = requests.post(
    f"{BASE}/v1/voice-design",
    headers={**HEADERS, "Content-Type": "application/json"},
    json={"instruction": instruction, "reference_text": reference_text, "n": 1},
    timeout=180,
)
if r.status_code != 200:
    sys.exit(f"Design failed HTTP {r.status_code}: {r.text[:300]}")
candidate = r.json()["candidates"][0]
wav = base64.b64decode(candidate["audio_base64"])
with open("design_sample.wav", "wb") as f:
    f.write(wav)
print(f"Candidate {candidate['duration_ms']}ms，WAV {len(wav)} bytes")

r = requests.post(
    f"{BASE}/model",
    headers=HEADERS,
    data={"type": "tts", "title": "design-demo-delete-me", "visibility": "private", "train_mode": "fast"},
    files={"voices": ("design_sample.wav", wav, "audio/wav")},
    timeout=180,
)
if r.status_code != 201:
    sys.exit(f"Persistence failed HTTP {r.status_code}: {r.text[:300]}")
voice_id = r.json()["_id"]
print("Persisted voice", voice_id, r.json().get("state"))
try:
    t = requests.post(
        f"{BASE}/v1/tts",
        headers={**HEADERS, "Content-Type": "application/json", "model": "s2-pro"},
        json={"text": "这是用设计出来的声音合成的一句话。", "reference_id": voice_id, "format": "mp3"},
        timeout=120,
    )
    if t.status_code != 200:
        sys.exit(f"Synthesis with new voice failed HTTP {t.status_code}: {t.text[:300]}")
    with open("design_voice_tts.mp3", "wb") as f:
        f.write(t.content)
    print(f"OK designed-voice synthesis {len(t.content)} bytes -> design_voice_tts.mp3")
finally:
    if not keep:
        d = requests.delete(f"{BASE}/model/{voice_id}", headers=HEADERS, timeout=30)
        print("Deleted test voice:", d.status_code)
