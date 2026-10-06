---
name: fish-api-tts
description: Generate speech with the Fish Audio REST API, including voice IDs, dialogue, reference audio, SSE alignment and live WebSocket examples. Use for developer integration and TTS debugging. Read fish-api-setup first.
---

# Text-to-Speech API

**Evidence:** the original 2026-10-03 notes report eleven regression cases passing across the API Skills and user listening approval for dialogue/reference-clone audio. The original run log and audio review record are not packaged in this release. Sample assertions and source notes are historical evidence; they do not independently verify every field or this English revision.

## Basic request

`POST https://api.fish.audio/v1/tts` with JSON and `Authorization: Bearer <FISH_API_KEY>`. Select the model using the **`model` HTTP header**, not the JSON body. Use `examples/basic_tts.py` from this Skill's directory (requires requests).

```bash
curl https://api.fish.audio/v1/tts \
  -H "Authorization: Bearer $FISH_API_KEY" \
  -H "Content-Type: application/json" -H "model: s2-pro" \
  -d '{"text":"Hello, welcome to Fish Audio.","format":"mp3"}' -o out.mp3
```

The example preserves the historically tested s2-pro identifier. Discover currently supported models before selecting one for a new integration. A missing/misspelled model header historically fell back silently, so validate the identifier yourself. No reference_id uses a default voice; a reusable voice ID comes from `fish-api-voices`.

## Parameters recorded in the legacy notes

| Field | Behavior / caveat |
|---|---|
| `text` | Required; do not rely on empty-text success |
| `reference_id` | Voice ID; array for supported multi-speaker models |
| `references` | Reference audio and transcript; use MessagePack, not JSON/base64 |
| `format` | mp3, wav, pcm or opus in the recorded interface |
| `sample_rate` | Must match format; check current valid combinations |
| `mp3_bitrate` | Recorded 64 / 128 / 192 |
| `latency` | Recorded normal / balanced / low |
| `temperature`, `top_p` | Validate documented range; silent acceptance is not proof an invalid value is supported |
| `prosody` | speed, volume and normalize_loudness; historical speed range 0.5–2.0 |
| `normalize`, `chunk_length` | Text normalization and chunk size; check current schema |

Recorded format/rate cases: MP3 32000/44100; WAV 8000/16000/24000/32000/44100; Opus 48000; PCM 16000/24000/44100. These observations do not certify every current combination. Speed observations were single stochastic samples, not a linear duration guarantee.

## Multiple speakers

For a supported S2-family model, provide an array of voice IDs and `<|speaker:N|>` markers corresponding to array positions. See `examples/dialogue.py`. Legacy s1 rejected an array; its error mentioned MessagePack even when the underlying problem was multi-speaker support. Check model capability rather than changing transport solely because of that message.

## Reference-audio cloning

Use `examples/zero_shot_clone.py` with msgpack. Pack a body containing text, format and `references=[{audio: audio_bytes, text: exact_reference_transcript}]`, with use_bin_type=True and `Content-Type: application/msgpack`. JSON/base64 was rejected in the recorded case. Use only authorized voice material. For repeated use, create a reusable private voice rather than retransmitting the recording every time.

## SSE timestamps

`POST /v1/tts/stream/with-timestamp` historically returns `text/event-stream`. See `examples/sse_timestamps.py`.

- Decode `audio_base64` chunks and concatenate in arrival order.
- Alignment is a cumulative snapshot for a chunk_seq: later data replaces earlier data for that chunk rather than appending it.
- Absolute segment time is chunk_audio_offset_sec + segment.start, in seconds.
- The observed alignment was character-level Chinese and word-level English, excluding punctuation.
- For requests, explicitly decode SSE text as UTF-8; a default ISO-8859-1 interpretation can corrupt Chinese text.
- TTS alignment is preferable to later ASR when captioning its own generated speech. This REST capability is not implied by basic MCP TTS availability.

## Live WebSocket

The recorded paths are `/v1/tts/live` and `/v1/tts/live/with-timestamp` on wss://api.fish.audio. Use Bearer/model handshake headers. See `examples/ws_live.py` (requires websockets and msgpack).

Send MessagePack frames: start with request → one or more text frames → flush → stop. Receive audio frames with binary audio and, on the timestamp path, content/alignment/chunk_seq/chunk_audio_offset_sec; finish carries a stop/error reason. A null alignment is not a new snapshot. Handle error frames and disconnects explicitly. Do not treat a partial audio stream as a complete deliverable.

## Errors, billing and limits

Check the API wallet before debugging parameters; 401 means invalid credentials, 402 insufficient API funds and 429 concurrency exhaustion. Correct invalid format/rate/latency or reference transport on 400. For a failed or uncertain paid call, record the original request/result and assess replay risk before retrying.

Historical TTS billing matched UTF-8 input bytes for the recorded models. Query current pricing rather than copying an old dollar price; wait for ledger updates before claiming reconciled charges. The API wallet is separate from MCP platform credits.

## Historical regression claim

The old notes report key check, basic synthesis, long sample, reference ID, dialogue, reference cloning, SSE timestamps, WebSocket, ASR, voice CRUD and voice design: 11 PASS / 0 FAIL. The retained historical runner is available to maintainers, but it was not executed during translation. It includes paid calls and automatic transport retries, so do not run it without reviewing replay risk and obtaining current spending authorization.
