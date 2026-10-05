---
name: fish-api-voices
description: |
  教开发者用 Fish Audio REST API 管理音色库：列出/搜索公开音色拿 reference_id、查询详情、
  创建（克隆）私有音色、删除。Use when 要选音色、把用户的声音样本变成可反复使用的音色、
  清理测试音色、搞清 reference_id 从哪来。需先通过 fish-api-setup。读者=开发者。
---

# Fish Audio 音色库 API · v0.1

对标：ElevenLabs voices。验证状态：端点与字段 2026-10-03 真 key 实测（含完整创建→查询→删除→再查 404 闭环）；`examples/voice_crud.py` 由 `evals/api-samples/run_all.sh` 回归。

> 前置：`fish-api-setup`。音色在 API 里叫 **model**（`type=tts`），TTS 的 `reference_id` 就是音色的 `_id`。

## 事实
- 音色库与 MCP **共享账号**：MCP 里克隆的音色，REST `GET /model?self=true` 立刻可见；MCP 里用的音色 id 也能直接当 REST 的 `reference_id`（实测）。钱包不共享。
- 创建、查询、删除音色实测未观察到扣费。

## 列出 / 搜索
```bash
curl "https://api.fish.audio/model?page_size=3&sort_by=task_count&language=zh" -H "Authorization: Bearer $FISH_API_KEY"
curl "https://api.fish.audio/model?self=true&page_size=5" -H "Authorization: Bearer $FISH_API_KEY"   # 只看自己的
```
响应：`{"total": 1002, "items": [{"_id": "...", "title": "...", "languages": ["zh"], "type": "tts", "visibility": "public", ...}]}`（中文公开音色实测共 1002 个）。已验证的查询参数：`page_size`、`sort_by=task_count`、`language`、`self=true`；其余筛选参数未验证。

## 查询
`GET /model/{id}` → 200，字段含 `title`、`description`、`languages`、`visibility`、`state`、`train_mode`、`cover_image`、`tags`。

## 创建（克隆）私有音色
`POST /model`，`multipart/form-data`，**必填四项**（缺任一返回 422）：

| 字段 | 取值 |
|---|---|
| `type` | `tts` |
| `title` | 音色名 |
| `train_mode` | `fast`（实测创建后立刻 `state: trained`） |
| `voices` | 样本音频文件（实测 10.5 秒清晰中文人声可用） |

可选 `visibility`（实测 `private` 可用）。成功返回 **201** 与音色对象，耗时约 6 秒。
```bash
curl -X POST https://api.fish.audio/model -H "Authorization: Bearer $FISH_API_KEY" \
  -F type=tts -F title=my-voice -F visibility=private -F train_mode=fast -F voices=@sample.mp3
```

## 删除
`DELETE /model/{id}` → **204**；之后再 `GET` → 404。

## 两种用法的取舍
| | 建音色（本页） | 零样本克隆（`fish-api-tts`） |
|---|---|---|
| 做法 | 一次上传，之后 `reference_id` 复用 | 每次请求都带参考音频（MessagePack） |
| 适合 | 固定角色音色、反复使用 | 一次性、用户即时上传 |
| 代价 | 占音色槽位 | 每次传输音频 |

## 合规
克隆他人声音须取得本人授权；MCP 的克隆接口有 `confirm_voice_rights` 确认，REST 创建接口未见该字段，责任在调用方。

## 未验证
音色槽位数量上限（站内同类接口按套餐限制并返回 429）、`public` / `unlist` 可见性的创建、样本最短时长、`enhance_audio_quality` 等可选字段。
