---
name: fish-api-voice-design
description: Design a new voice from a written description using the Fish Audio REST API. Use to generate audition candidates and optionally persist an authorized candidate as a reusable voice. Read fish-api-setup first.
---

# Voice Design API

**Evidence:** legacy real-key notes dated 2026-10-03 report synchronous candidate generation and a design → create model → TTS → delete lifecycle. The original eleven-case regression log has not been recovered. This English revision is not newly execution-tested; optional parameters and invoices are not fully verified.

## Design candidates

`POST https://api.fish.audio/v1/voice-design` with JSON, Bearer authentication and no model header in the recorded successful case. Run `examples/design.py` from this Skill's directory when authorized.

```bash
curl https://api.fish.audio/v1/voice-design \
  -H "Authorization: Bearer $FISH_API_KEY" -H "Content-Type: application/json" \
  -d '{"instruction":"Warm, calm English narration","reference_text":"Welcome to the demonstration.","language":"en","n":1}'
```

Historical schema fields: required `instruction` (1–2000 characters), optional `reference_text` (up to 150 characters), language, candidate count n (1–4, default 2), speed, num_step, guidance_scale, instruct_guidance_scale and seed. Verify current schema for exact ranges; the successful n=1 case does not establish all parameter combinations. Unknown-field rejection came from source inspection, not a recorded negative execution test.

The response contains `candidates`, including id/index, `audio_base64`, sample_rate, duration_ms, text, language and voice-description metadata. The recorded audio decoded to a complete 44.1 kHz WAV container. Do not interpret signature/token fields as public API keys.

## Reuse a candidate

Candidate generation does not automatically persist a voice. Decode its WAV, then use the authorized private `POST /model` flow from `fish-api-voices`. The returned `_id` can be used for TTS. `examples/design_to_voice.py` demonstrates the lifecycle and deletes its test model; preserve the ID for safe cleanup. The historical public model creation did not require the voice-design signature.

Use an audition text long enough for a meaningful listening review; one candidate or a 200 response does not prove the requested voice quality. Retrieve current pricing and confirm the authorized spend before generation. The legacy price note was per successful design request, not per returned candidate, and was not independently invoice-tested.
