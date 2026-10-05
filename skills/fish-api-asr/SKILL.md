---
name: fish-api-asr
description: |
  教开发者用 Fish Audio REST API 做语音转文字（ASR）：上传音频文件，拿到文本、词/字级时间戳、
  说话人分段（speaker_turns）。Use when 要写代码转写音频、做字幕/对齐、会议或多人对话转写、
  长录音（最长 60 分钟）、排查 segments 为空 / 没有说话人标记 / 503 / 对比 MCP speech_to_text。
  需先通过 fish-api-setup。读者=开发者。
---

# Fish Audio 语音转文字（ASR）API · v0.2

对标：ElevenLabs speech-to-text。验证状态：2026-10-03 真 key 实测 + 官方文档交叉核对；`examples/transcribe.py` 由 `evals/api-samples/run_all.sh` 回归。

> 前置：`fish-api-setup`。端点 `POST /v1/asr`，`multipart/form-data`（或 `application/msgpack`；**不接受 JSON + base64**）。

## ⚠️ 先选模型：`model` 请求头（不是表单字段）
| 头值 | 适用 | 限制 |
|---|---|---|
| `transcribe-1-pro`（**推荐**） | 多人对话、长录音、情绪/事件标记 | 单文件 ≤ 60 分钟；长音频可能跑几分钟 |
| `transcribe-1`（头缺失或写错时的**静默默认**） | 短录音通用转写 | ≤ 50 MiB；时间长会 **503**（实测 95 秒音频 44 秒后 503） |

- 头值必须**小写完全匹配**；`Transcribe-1-Pro`、`transcribe-1pro` 都不会报错，而是**悄悄按 transcribe-1 处理和计费**。拿到的 `text` 里没有 `<|speaker:N|>` 标记就先查这个头。
- 表单里写 `model=...` 会被忽略。
- 旧版本本页写过"无需 model 头"——那只对短音频成立（会落到 transcribe-1），长音频和说话人分段必须带头。

## 快速上手（`examples/transcribe.py`，需 `pip install requests`）
```python
import os, requests
with open("audio.mp3", "rb") as f:
    r = requests.post("https://api.fish.audio/v1/asr",
        headers={"Authorization": f"Bearer {os.environ['FISH_API_KEY']}", "model": "transcribe-1-pro"},
        files={"audio": f},
        data={"ignore_timestamps": "false", "language": "zh"},
        timeout=900)          # 长音频要长超时；requests 默认无超时，httpx 默认仅 5 秒
r.raise_for_status()
res = r.json()
for t in res.get("speaker_turns", []):
    print(t["speaker"], f'{t["start"]:.2f}-{t["end"]:.2f}', t["text"])
```
```bash
curl -X POST https://api.fish.audio/v1/asr -H "Authorization: Bearer $FISH_API_KEY" -H "model: transcribe-1-pro" \
  -F audio=@audio.mp3 -F ignore_timestamps=false -F language=zh
```

## 请求字段（pro；multipart 与 msgpack 同名）
| 字段 | 默认 | 说明 |
|---|---|---|
| `audio` | 必填 | 恰好一个文件；格式从字节内容识别，不看扩展名。支持 WAV/MP3/AAC(M4A)/FLAC/Ogg/WebM/MOV；AIFF/WMA/AMR/裸 PCM → 400 |
| `language` | 空 | 小写 ISO 639-1（`zh` `en` `ja`）；仅提示，仍会自动检测；`en-US`、`English` 可能 400 |
| `ignore_timestamps` | **true** | 默认 `segments` 为空；要时间戳显式传 `false`。multipart 里**除 `true` 外任何值都算 false** |
| `tag_audio_events` | true | `false` 去掉 `[laughter]`、`[高兴]` 等括号标记（时间戳与计费不变） |
| `diarize` | auto | `false` 则不返回 `speaker_turns` |
| `num_speakers` / `min_speakers` / `max_speakers` | 空 | 说话人数提示，尽力而为（短录音可能无效）；`num_speakers` 不能与 min/max 同传；与 `diarize=false` 同传 → 400 |
| `transcribe-1` 只认 | | `audio`、`language`、`ignore_timestamps`；其余字段仅 pro |

## 响应（pro，`ignore_timestamps=false`；下为实测）
```json
{"text": "<|speaker:0|>早上好。 <|speaker:1|>早上好，[疑问]你好吗？ <|speaker:0|>很好，谢谢。",
 "duration": 4.336, "language": "Chinese", "language_code": "zh", "request_id": "0f4b70b1-…",
 "segments": [{"text": "早", "start": 0.0, "end": 0.16}, "…"],
 "speaker_turns": [{"speaker": "speaker:0", "text": "早上好。", "start": 0.0, "end": 0.88},
                   {"speaker": "speaker:1", "text": "早上好，[疑问]你好吗？", "start": 1.04, "end": 2.56},
                   {"speaker": "speaker:0", "text": "很好，谢谢。", "start": 2.88, "end": 4.0}]}
```
- 时间单位**秒**（SDK 的 Python docstring 写成毫秒，是错的）。`segments` 中文逐字、英文逐词，不含标点/标记。
- 取说话人**用 `speaker_turns`，别解析 `text`**；`speaker:N` 只在单次响应内有效，**整段对话要一次发完**，分多次发标签不连续。
- `request_id` 同时在 `x-request-id` 响应头和错误体里，反馈问题时附上。
- 实测：2 人对话（4.3 秒，`num_speakers=2`）→ 3 个 turn、说话人切换正确，1.2 秒返回；95 秒单人音频 → 200、84 段，28 秒返回（同音频 transcribe-1 是 503）。

## 错误处理（pro：按 HTTP 状态 + `code` 分支，别按 `message`）
| 状态 | `code` | 处置 |
|---|---|---|
| 400 | `invalid_request` `invalid_parameter` `invalid_audio` `audio_too_long`(>60 分钟) `audio_too_short`(<约 0.08 秒) | 改请求，**不要重试** |
| 413 | `request_too_large`（可能来自网关，无 JSON） | 发压缩音频（MP3/Opus/AAC，1 小时 128kbps MP3 约 55 MiB） |
| 415 | `unsupported_media_type` | 用 multipart 或 msgpack |
| 429 | 并发满 | 指数退避，无 `Retry-After`；**每个 ASR 请求占一个并发槽直到返回** |
| 500/502/503/504 | `upstream_unavailable` `upstream_timeout` `excessive_repetition` `diarization_failed`… | 指数退避重试 |

## 与 MCP `speech_to_text` 的区别
| | REST `/v1/asr` | MCP `speech_to_text` |
|---|---|---|
| 时间戳 | `ignore_timestamps=false` 得词/字级 + 说话人分段 | 不返回 |
| 文本标记 | pro：带 `<|speaker:N|>` 与 `[情绪]`；transcribe-1：干净文本 | 观察到带 `<|speaker:0|>` 与 `[回声]` 类标记 |
| 钱包 | API 余额 | 平台 credits |
→ 要时间戳、说话人分段或长音频，走 REST。

## 字幕用哪个时间戳
给 **TTS 生成的音频**配字幕，用 TTS 的时间戳（`fish-api-tts` 的 SSE/WebSocket，生成时对齐）；给**别人录的音频**配字幕才用 ASR。同一句话两者数值略有出入（实测"欢"字：TTS 1.20–1.52s，ASR 1.04–1.36s）。

## 价格
官方定价 **$0.36 / 音频小时**（两个模型同价，按秒向上取整，整段含静音计费，**返回错误的请求不计费**）。本页未做账单实测。

## 未验证
msgpack 请求体、`tag_audio_events=false`、`min/max_speakers`、>5 分钟的长音频、非 mp3 格式。
