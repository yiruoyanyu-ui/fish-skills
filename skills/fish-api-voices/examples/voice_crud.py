"""音色全流程：创建私有音色 → 查询 → 删除（再查应 404）。
用法: python voice_crud.py sample.mp3 [标题]
样本建议 10 秒左右的清晰人声；创建后 state 立刻为 trained（train_mode=fast）。"""
import os
import sys

import requests

BASE = "https://api.fish.audio"
HEADERS = {"Authorization": f"Bearer {os.environ['FISH_API_KEY']}"}
sample = sys.argv[1]
title = sys.argv[2] if len(sys.argv) > 2 else "api-sample-delete-me"

with open(sample, "rb") as f:
    r = requests.post(
        f"{BASE}/model",
        headers=HEADERS,
        data={"type": "tts", "title": title, "visibility": "private", "train_mode": "fast"},
        files={"voices": f},
        timeout=180,
    )
if r.status_code != 201:
    sys.exit(f"创建失败 HTTP {r.status_code}: {r.text[:300]}")
voice_id = r.json()["_id"]
print("created", voice_id, r.json().get("state"))
try:
    g = requests.get(f"{BASE}/model/{voice_id}", headers=HEADERS, timeout=30)
    assert g.status_code == 200 and g.json()["title"] == title, g.text[:200]
    print("get ok:", g.json().get("state"), g.json().get("visibility"))
finally:
    d = requests.delete(f"{BASE}/model/{voice_id}", headers=HEADERS, timeout=30)
    print("delete:", d.status_code)
assert d.status_code == 204, d.status_code
g2 = requests.get(f"{BASE}/model/{voice_id}", headers=HEADERS, timeout=30)
assert g2.status_code == 404, g2.status_code
print("deleted; 再查 404")
