---
name: fish-api-voice-design
description: |
  用文字描述生成全新音色（Fish 特色能力）：POST /v1/voice-design，同步返回 1–4 个带 WAV 音频的
  候选音色。Use when 开发者要"按描述生成声音"、做角色音色选择器、了解设计出的声音能否持久化复用。
  需先通过 fish-api-setup。读者=开发者。
---

# Fish Audio 声音设计 API · v0.1

验证状态：请求/响应结构 2026-10-03 真 key 实测，字段定义取自 `fish-platform-api` 源码；`examples/design.py` 由 `evals/api-samples/run_all.sh` 回归。ElevenLabs 无同名公开接口，本页无直接对标。

> 前置：`fish-api-setup`。`POST /v1/voice-design`，JSON，**同步**返回，**无需 `model` 头**（实测）。

## 快速上手（`examples/design.py`）
```bash
curl -X POST https://api.fish.audio/v1/voice-design -H "Authorization: Bearer $FISH_API_KEY" -H "Content-Type: application/json" \
  -d '{"instruction":"温暖沉稳的中文男声旁白","reference_text":"一键弹盖，仰头就喝。","language":"zh","n":1}'
```

## 请求字段
| 字段 | 说明 |
|---|---|
| `instruction` | 必填，1–2000 字，音色描述 |
| `reference_text` | 可选，≤150 字，候选念的内容（也就是试听文本） |
| `language` | 可选，BCP-47 提示（`zh`/`en`/`ja`） |
| `n` | 候选数，1–4，默认 2 |
| `speed` | 语速倍率，(0, 3]，默认 1.0 |
| `num_step` | 扩散步数，1–128，默认 32 |
| `guidance_scale` | ≥0，默认 2.0，越大越贴合描述 |
| `instruct_guidance_scale` | ≥0，默认 0.0 |
| `seed` | 可选，固定随机性 |
源码里 schema 为 `extra=forbid`（多传未知字段会被拒，未实测）。

## 响应（`candidates[]`）
| 字段 | 说明 |
|---|---|
| `id` / `index` | 候选标识 / 序号 |
| `audio_base64` | 解码后是**完整 WAV 容器**（实测 44.1kHz） |
| `sample_rate` / `duration_ms` | 采样率 / 时长 |
| `text` / `language` | 实际念的内容 / 语言 |
| `instruct` | 模型对这个声音的结构化描述（性别、年龄、语气、情绪、语速…） |
| `features` | 同上的结构化字段：`gender` `age` `tone` `emotion` `pacing` `accent` `loudness` `reverb` `speed_factor` `description` |
| `audio_token_sha256` / `signature` | 服务端校验用（`v1:` + HMAC-SHA256(服务端密钥, WAV 的 sha256)），客户端无需验证 |
实测 `n=1`：4.7 秒返回，1.86 秒音频。

## 把候选变成可复用音色
**可以，且已实测完整闭环**（`examples/design_to_voice.py`）：设计 → 取候选 `audio_base64` 解码出 WAV → 当作 `voices` 样本走公开的 `POST /model`（multipart：`type=tts`、`title`、`visibility=private`、`train_mode=fast`、`voices=@candidate.wav`）→ 返回 201 与 `_id`（约 6 秒 `state=trained`）→ 把 `_id` 作为 `reference_id` 调 `/v1/tts` 合成成功 → `DELETE /model/{id}` 得 204。
- 设计结果本身**不会自动保存**：不持久化，候选只存在于这次响应里。
- 候选 WAV 越长越稳；`reference_text` 建议写到能念满 8 秒以上。
- `signature` 是服务端校验用的，走公开 `POST /model` 持久化时不需要。

## 价格
官方定价 **$0.01 / 次成功请求**（模型 `voice-design-1`）：一次请求返回 1–4 个候选只计一次，所以**要多个候选就把 `n` 开大，不要多次调用**；鉴权、参数、余额、并发、服务端错误都不计费。本页未做账单实测。
