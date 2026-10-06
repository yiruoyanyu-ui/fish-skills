---
name: fish-api-voices
description: List, inspect, create and delete Fish Audio voice models through REST. Use to obtain a TTS reference_id or manage an authorized private voice. Read fish-api-setup first.
---

# Voice Library API

**Evidence:** legacy real-key notes dated 2026-10-03 report create → inspect → delete → 404, using a short Chinese voice sample. The original regression log is not packaged. Optional visibility modes and account limits are not validated by that case.

A voice is an API `model` of `type=tts`. Its `_id` is the `reference_id` used by TTS. The historical account could see its MCP-created voices through REST; its API and platform wallets remained separate.

## Discover and inspect

```bash
curl "https://api.fish.audio/model?page_size=3&sort_by=task_count&language=en" \
  -H "Authorization: Bearer $FISH_API_KEY"
curl "https://api.fish.audio/model?self=true&page_size=5" \
  -H "Authorization: Bearer $FISH_API_KEY"
```

The response contains `total` and `items` with `_id`, title and metadata. Historical query coverage includes page_size, sort_by, language and self. Library counts are dynamic, not constants. `GET /model/{id}` returns voice metadata including visibility/state.

## Create a private voice

Use only a recording that the user is authorized to use for cloning. Obtain that authorization before creating a voice; a REST endpoint lacking a confirmation flag does not waive the requirement.

`POST /model`, multipart form data, with `type=tts`, `title`, `train_mode=fast` and one `voices` file. Set `visibility=private`. The historical successful case returned 201 and a trained voice.

```bash
curl https://api.fish.audio/model -H "Authorization: Bearer $FISH_API_KEY" \
  -F type=tts -F title=test-voice -F visibility=private \
  -F train_mode=fast -F voices=@authorized-sample.mp3
```

Use `examples/voice_crud.py` from this Skill's directory for the lifecycle sample. It creates and then deletes its test voice; do not use an existing user's voice as a disposable fixture.

`DELETE /model/{id}` historically returned 204, followed by 404 on lookup. Delete only the voice owned by this authorized operation. Record the created ID so cleanup can target the original resource after interruption.

For repeated use, create a reusable model and pass its ID. For a one-off reference, see MessagePack reference audio in `fish-api-tts`. Historical create/read/delete tests observed no charge; do not treat that observation as a current pricing promise.

Untested: slot limits, public/unlisted voice creation, minimum sample duration and enhancement options.
