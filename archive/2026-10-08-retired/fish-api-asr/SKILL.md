---
name: fish-api-asr
description: Transcribe recorded audio with the Fish Audio REST API, including timestamps and speaker turns. Use for transcription code, alignment and ASR troubleshooting. Read fish-api-setup first.
---

# Speech-to-Text API

**Evidence:** the original notes report real-key tests on 2026-10-03, including a short two-speaker clip and a 95-second recording. The original regression run log is not packaged; long recordings, formats and optional parameters have incomplete coverage. This English revision has not been executed independently.

## Request

Endpoint: `POST https://api.fish.audio/v1/asr`. Authentication: `Authorization: Bearer <FISH_API_KEY>`. Use multipart form data; the historical interface also supports MessagePack, but that ASR path was not tested. Do not send JSON/base64 audio.

Select the model using the **`model` HTTP header**, not a form field. The historical preferred path for speaker turns and longer audio is `transcribe-1-pro`. The old notes observed a silent fallback to `transcribe-1` for a missing or misspelled header; validate the identifier against current documentation rather than relying on an error.

Use `examples/transcribe.py` from this Skill's directory. It requires requests and a local audio file. Example:

```bash
curl https://api.fish.audio/v1/asr \
  -H "Authorization: Bearer $FISH_API_KEY" -H "model: transcribe-1-pro" \
  -F audio=@audio.mp3 -F ignore_timestamps=false -F language=en
```

| Field | Historical behavior |
|---|---|
| `audio` | One file; recognition uses its bytes, not its extension |
| `language` | Optional lower-case language hint such as en, zh or ja |
| `ignore_timestamps` | Defaults true; explicitly send false for timestamps |
| `tag_audio_events` | Audio-event tags; optional false path not tested |
| `diarize` | Speaker turns; false suppresses them |
| `num_speakers`, `min_speakers`, `max_speakers` | Best-effort hints; do not combine num with min/max or hints with diarize=false |

The historical pro limit was 60 minutes; tests only reached 95 seconds. Check current size/duration limits and allow a sufficient timeout for long audio.

## Interpret the response

- `text` is the transcript; pro output can include speaker and emotion/event markers.
- `segments` contains character/word timing in **seconds**. Do not assume punctuation has a segment.
- Use `speaker_turns` for diarization, rather than parsing speaker tags in text. A speaker identifier is local to one response; chunking an entire conversation into separate requests does not preserve identity automatically.
- Preserve `request_id` / `x-request-id` when reporting a problem.
- For captions on TTS-generated audio, prefer the TTS generation alignment when available. ASR alignment is appropriate for an existing recording and can differ from TTS timing.

## Errors and limits

Correct invalid request/audio/parameter errors rather than retrying unchanged input. For a 413, compress or split within the task's requirements. A 415 indicates the wrong content type. A 429 requires concurrency control and backoff. For server or transport failures, consider whether the original paid operation is known before repeating it; do not assume unlimited safe retries.

REST timestamps/speaker turns are distinct from the legacy MCP `speech_to_text` response, which did not expose those timestamps. API wallet billing is distinct from platform credits. Check current prices; the legacy notes did not reconcile an ASR invoice.

Not independently covered: MessagePack ASR, audio-event suppression, min/max speakers, recordings longer than five minutes and non-MP3 formats.
