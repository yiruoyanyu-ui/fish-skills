---
name: ugc-product-video
description: Make a product-led short promotional video with voice-over from a real product reference and a specified duration. The evaluated scope is a faceless product video, not presenter reviews, unboxing, tutorials or try-on. Do not use to edit an existing video.
---

# UGC Product Video

**Validation:** the legacy record reports one complete Fish 10-second product-video run on 2026-10-04. It does not validate all durations, product categories, presenters or all six HF UGC formats. Original runtime evidence is not packaged in this release; see the validation inventory. This English revision has not undergone a new Agent execution test.

Read `../shared/core-skeleton.md`. This recipe adapts storyboard, voice-over budgeting and product intake concepts. It does not install HF cloud scripts or run an autonomous backend workflow.

## Execution platform and discovery

Use Fish execution tools when the task authorizes Fish credits. Use HF only if the user explicitly requests it and that connection is available; disclose the platform. If ambiguous, clarify once. Discover current models, reference roles, supported duration/resolution/audio parameters and prices before submission. Legacy observations are not current quotes.

The historical Fish path used a gpt-image-2 storyboard, a reference-video mode and separate TTS, followed by local assembly. Do not assume model IDs or a reference-video mode are currently available. A model that only accepts a start frame cannot execute the multi-reference storyboard recipe.

## Workflow

1. Gather a real product photo and duration, preferably together. Offer 10/15/30/45 seconds when a choice is needed. Do not invent or substitute a reference. Set technical defaults from current tool capabilities rather than interviewing the user about model internals.
2. Write a canonical product description: visible mechanism, proportions relative to hands, visible faces, unknown features and treatment of promotional text/watermarks. Reuse it consistently. Avoid artificial perfection, but do not invent damage or redesign the product.
3. Write a segmented voice-over. The historical Chinese 10-second case used approximately 20–32 characters; other languages need their own measured timing. Use visible details and supplied facts, never fabricated specifications.
4. Create a four-panel storyboard in a 21:9 canvas with four vertical slots, if supported. Use the cleaned product reference. Plan reveal, demonstration A, demonstration B and outcome. Specify visible product angles, realistic scale, shot labels and concrete hand actions; prohibit extra hands, text and watermarks. Inspect equal panels, seams and missing placeholders. One regeneration is allowed only within user authorization; otherwise disclose a fallback.
5. Optional visual cleanup: skip and disclose when the board is only a reference and passes inspection. If used directly or visibly artificial, perform a targeted edit. Historical guidance allowed at most two edits; this is a limit, not automatic spending permission.
6. Generate video using the storyboard and clean product as **references**, not as the start frame. Write explicit shot windows, framing, action and hard cuts. Feeding a whole board as the starting frame can leave the board visible in the resulting video.
7. Generate separate voice-over segments using an available voice suited to the brief. Legacy voice IDs are not portable defaults; query or validate the current catalog. Disclose any substituted voice.
8. Detect actual scene cuts with ffmpeg rather than trusting planned windows. Align each voice segment with `adelay`; if it exceeds the shot window, use `atempo` up to 1.3 rather than truncating speech. Mix with `amix` and normalize=0; aim for no more than one second of trailing silence. If fitting needs a greater speed change, deliver video and narration separately.
9. Inspect extracted frames for shot structure, product consistency, text/watermarks and hands. Check cut count and duration within approximately 0.3 seconds of the selected target. Report listening review separately; user confirmation of voice quality is not implied by a successful tool response. Do not enter repeated environment-installation attempts merely to manufacture a QC result.
10. Save a preliminary delivery record before assembly. Final delivery includes media URLs/files, prompts, original task IDs, actual costs, platform, cut timings, speed adjustments, voice selection and any unfinished processing.

## Historical duration planning

| Duration | Boards | Planned segments |
|---|---|---|
| 4–15 seconds | 1 | Full length |
| 16–19 seconds | 2 | Balanced segments, each at least 4 seconds |
| 20–30 seconds | 2 | 15 seconds plus remainder |
| 31–45 seconds | 3 | 15, 15, remainder |
| 46–60 seconds | 4 | Approximately 15 each |

Only the single 10-second case is reported as tested. The table is planning guidance, not verified engine support.

## Recovery

Poll the original task when generation is slow or uncertain; do not create a second paid submission. If two authorized storyboard attempts fail inspection, offer a disclosed single-shot fallback. With native generated audio, a changed script may require full regeneration: explain the new operation and obtain applicable authorization before spending.
