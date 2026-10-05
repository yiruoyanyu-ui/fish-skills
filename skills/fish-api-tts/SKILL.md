---
name: fish-api-tts
description: |
  教开发者/Agent 用 Fish Audio REST API 做文本转语音：基础合成、输出格式与采样率、语速音量、
  多说话人对话、零样本克隆（MessagePack）、流式字/词级时间戳（SSE）、实时 WebSocket。
  Use when 要写代码调用 Fish TTS、需要字幕级时间戳、做对话/实时配音应用、选 model/format/参数、
  排查 400/402/429。需先通过 fish-api-setup 确认 key 与余额。
  读者=开发者；终端用户要成品音频请用 narration 页。
---

# Fish Audio TTS API · v0.2

对标：ElevenLabs text-to-speech（229 行）。验证状态：协议细节与数字均为 2026-10-03 真 key 实测；`examples/` 脚本由 `evals/api-samples/run_all.sh` 整体回归（结果见页尾）。

> **前置**：`fish-api-setup`（key、API 余额、钱包独立、并发上限、计费）。鉴权 `Authorization: Bearer <FISH_API_KEY>`；模型走**请求头 `model`**，不是 body 字段。

## 快速上手

### Python（`examples/basic_tts.py`，需 `pip install requests`）
```python
import os, requests
r = requests.post(
    "https://api.fish.audio/v1/tts",
    headers={"Authorization": f"Bearer {os.environ['FISH_API_KEY']}",
             "Content-Type": "application/json", "model": "s2-pro"},
    json={"text": "你好，欢迎使用 Fish Audio。", "format": "mp3"},   # 加 "reference_id" 指定音色
    timeout=120)
r.raise_for_status()
open("out.mp3", "wb").write(r.content)
```
### curl
```bash
curl -X POST https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" -H "Content-Type: application/json" -H "model: s2-pro" \
  -d '{"text":"你好，欢迎使用 Fish Audio。","format":"mp3"}' -o out.mp3
```
不传 `reference_id` 用默认音色；默认输出 mp3 / 44.1kHz / 单声道 / 128kbps。音色从哪来见 `fish-api-voices`。

## `model` 头（⚠️ 不校验）
| 头值 | 说明 |
|---|---|
| `s2.1-pro` | **官方推荐生产用**，也是缺省回落目标 |
| `s2.1-pro-free` | 免费档：同一模型，无首包延迟（TTFA）与可用性（DPA）保证，适合评估和原型；实测 SDK 调用 200 |
| `s2-pro` | 上一代 S2；本页示例沿用 |
| `s1` | 旧系：不支持多说话人数组；情绪标记用 `(happy)` 圆括号而非 S2 的 `[自然语言]` 方括号 |
| `drama-3-preview` | 预览模型，行为与可用性可能变 |
- **头缺失或写错 → 静默回落，不会 400**（实测 `not-a-model`、缺头都 200，且双人对话可用，与"回落到 S2 家族"一致；官方文档写明回落 `s2.1-pro` 并按其计费）。代码里用常量，别指望靠报错发现拼写错误。
- 多说话人需 S2 家族（`s2-pro`、`s2.1-pro`、`s2.1-pro-free`、`drama-3-preview`）；`s1` + 数组 `reference_id` → 400。`speech-1.5/1.6` 已弃用。
- 官方 SDK 的类型声明目前只列 `s1`/`s2-pro`（SDK 默认 `s2-pro`），但值不做运行时校验，`"s2.1-pro"` 能发出去，只是类型检查器会报。

## 请求体字段（均实测）
| 字段 | 默认 | 实测要点 |
|---|---|---|
| `text` | 必填 | 缺失 → 400 `missing field text`；空串 `""` 不报错（返回 200） |
| `reference_id` | — | 音色 `_id`；多说话人传数组 |
| `references` | — | 零样本克隆，**必须 MessagePack**（见下） |
| `format` | `mp3` | `mp3` `wav` `pcm` `opus`；其他（如 `flac`）→ 400 并列出可选值 |
| `sample_rate` | 按格式 | 见下表；不合法 → 400 并列出可选值 |
| `mp3_bitrate` | 128 | 64 / 128 / 192；其他 → 400 |
| `latency` | `normal` | `normal`（最优质）/ `balanced` / `low`；其他 → 400 |
| `temperature` / `top_p` | 0.7 | 文档范围 0–1；**`temperature=2` 实测不报错**（是否截断未知，别依赖） |
| `prosody` | — | `{speed 0.5–2.0, volume dB, normalize_loudness}`；speed 越界 → 400 `speed must be in [0.5, 2.0]` |
| `normalize` | true | 中英文数字规范化 |
| `chunk_length` | 300 | 100–300 |

### 格式 × 采样率（不合法组合 400，消息里列出可选值）
| format | 支持的 sample_rate |
|---|---|
| mp3 | 32000、44100（默认 44100） |
| wav | 8000、16000、24000、32000、44100 |
| opus | 48000（唯一） |
| pcm | 16000、24000、44100 已验证；8000/32000/48000 未测 |

### 语速（prosody.speed）
同一句话实测：0.8 → 6.7 秒，1.0 → 5.3 秒，1.5 → 2.8 秒（各 1 次；每次合成有随机性，非严格线性）。

## 多说话人对话（`examples/dialogue.py`）
```json
{"text": "<|speaker:0|>早上好！<|speaker:1|>早上好，你好吗？<|speaker:0|>很好，谢谢！",
 "reference_id": ["<音色A的id>", "<音色B的id>"]}
```
下标对应数组位置，用 `<|speaker:N|>` 切换。实测 `s2-pro` + 两个公开音色 → 200、4.3 秒音频，ASR 转写确认三句台词都被念出。两个声音是否分得开需人耳判断。旧系 `s1` + 数组 `reference_id` → 400 `Failed to parse the request body as MsgPack: data did not match any variant of untagged enum MultiSpeakerReference`——**消息提到 MsgPack 有误导**，实际原因是旧系不接受数组。

## 零样本克隆（MessagePack，`examples/zero_shot_clone.py`，需 `pip install msgpack`）
```python
body = msgpack.packb({"text": "新文本", "format": "mp3",
                      "references": [{"audio": audio_bytes, "text": "参考音频里说的原话"}]},
                     use_bin_type=True)
requests.post(url, headers={..., "Content-Type": "application/msgpack", "model": "s2-pro"}, data=body)
```
- JSON 无法携带音频：把 base64 字符串塞进 JSON → 400 `Reference Audio is not valid, please check your reference audio`。
- 实测：3 秒参考音频即可合成成功；建议 10–30 秒清晰人声，`text` 必须是参考音频的逐字文本。
- 想反复使用 → 建音色（`fish-api-voices`），不必每次传音频。

## 流式 + 字/词级时间戳（SSE，`examples/sse_timestamps.py`）
`POST /v1/tts/stream/with-timestamp`，请求体同 `/v1/tts`，返回 `text/event-stream`。每条事件 `data:` 后是 JSON：
`audio_base64`（音频块）、`content`（该 chunk 文本）、`alignment`（`segments[{text,start,end}]` + `audio_duration`）、`chunk_seq`、`chunk_audio_offset_sec`。
1. 所有 `audio_base64` 按到达顺序拼接 = 完整音频（实测与同文本非流式响应字节数一致，50154 B）。
2. `alignment` 是该 `chunk_seq` 的**累计快照**：后到的**覆盖**先到的，不要追加。
3. 绝对时间 = `chunk_audio_offset_sec + segment.start`。
4. 粒度（实测）：**中文逐字、英文逐词**，标点不在 segments 里；"你好，欢迎使用 Fish Audio。" → 你/好/欢/迎/使/用/Fish/Audio 共 8 段。
5. ⚠️ Python `requests` 对 `text/event-stream` 默认按 ISO-8859-1 解码，**必须 `r.encoding = "utf-8"`**，否则中文乱码。
6. 这是给 TTS 音频配字幕 / 卡拉 OK / 口型对齐的首选来源（比事后 ASR 更贴合）。**MCP 层未暴露此能力**，需要时走 REST。

## 实时 WebSocket
**不需要时间戳**时用基础端点 `wss://api.fish.audio/v1/tts/live`（官方标准路径）：帧协议相同，服务端只回 `audio`（字段 `audio`/`event`/`time`）与 `finish`。实测 start → 2 段 text → flush → stop → 6 个 audio 事件 + `finish(stop)`，共 50990 字节。下面是**带时间戳**的变体：

### 带时间戳（`examples/ws_live.py`，需 `pip install websockets msgpack`）
`wss://api.fish.audio/v1/tts/live/with-timestamp`，握手头同 REST（`Authorization`、`model`）。帧是 **MessagePack**（不是 JSON；音频是 msgpack `bin`，不是 base64）。
- 客户端发：`{"event":"start","request":{...同 /v1/tts 的 body，text 可为空}}` → 若干 `{"event":"text","text":"..."}` → `{"event":"flush"}`（立即合成缓冲文本）→ `{"event":"stop"}`。
- 服务端回：`{"event":"audio","audio":bytes,"content","alignment"|null,"chunk_seq","chunk_audio_offset_sec","time"}` → `{"event":"finish","reason":"stop"|"error"}`；请求级失败发 `{"event":"error","error",...}` 后关闭。
- `alignment` 语义同 SSE（累计快照覆盖；`null` 表示该 chunk 暂无变化）。
- 实测：3 段文本 → 8 个 audio 事件 + 1 个 `finish(stop)`，1.4 秒内完成，拼接音频 4.02 秒；文本被切成 2 个 chunk（chunk 1 的 offset = 2.74 秒）。

## 错误速查（全部实测）
| 现象 | 原因 | 处置 |
|---|---|---|
| 401 Invalid Token | key 无效 | `fish-api-setup` |
| 402 | API 余额不足（钱包独立） | 充值；先 `GET /wallet/self/api-credit` |
| 429 | 并发超过上限（实测 5） | 限流 + 退避 |
| 400 `unknown variant X, expected one of ...` | `format` / `latency` 取值错 | 用消息里列的值 |
| 400 `Invalid sample rate N for format F. Supported ...` | 格式与采样率不匹配 | 见上表 |
| 400 `Reference Audio is not valid` | 零样本用 JSON 发了 | MessagePack |
| 400 `...untagged enum MultiSpeakerReference` | 旧系模型 + 数组 `reference_id` | 换 `s2-pro` |
| 200 但"参数没生效" | `model` 头写错 / `temperature` 越界都不报错 | 用常量、自行校验范围 |
| curl 35 / HTTP 000 | 本地 TLS 抖动 | 退避重试 |

## 计费
`s2.1-pro` / `s2-pro` / `s1`：**$15 / 百万 UTF-8 字节**（官方价目；实测 s2-pro、s1、缺省头均吻合）。`s2.1-pro-free`：$0（实测未见扣费）。中文每字 3 字节。入账有延迟，见 `fish-api-setup`。

## 回归结果
2026-10-03 `evals/api-samples/run_all.sh`：**11 PASS / 0 FAIL**（key 校验、基础合成、长样本、reference_id、多说话人、零样本克隆、SSE 时间戳、WebSocket、ASR、音色 CRUD、声音设计）。对话与零样本克隆的音频已由用户人耳确认「声音没问题」。整套约 $0.02，需环境变量 `FISH_API_KEY`。
