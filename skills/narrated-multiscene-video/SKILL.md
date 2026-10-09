---
name: narrated-multiscene-video
description: Produce a complete narrated story or explainer across multiple scenes, coordinating reusable visual references, shot order, voice and assembly. Use for multiscene stories and educational channel videos; product demonstrations use UGC and source-action transfer uses video recreation.
---

# Narrated Multiscene Video · v0.1-candidate.6

Research candidate; new media artifact acceptance is pending.

## Plan the film and each state change

Reuse the topic/script, audience, style, duration, ratio and sound choices. Match the requested scope: a plan request returns a plan; a film request requires one playable assembled video. Keep factual explanations supported and proposed creative choices distinct from supplied facts. Choose scenes to tell the beginning, change and payoff within the brief, without fixed cuts or durations.

For each state-dependent scene, record three separate fields: starting state → ordered action → ending state, alongside its subject, input source, narration and time window. Derive the image prompt from the starting state and the video prompt from the ordered action. Before finalizing the pair, compare the actual descriptions: does the frame permit the first action, is the action already complete, and does its result match the next scene? Revise any contradictory pair before generating. Independent scenes may intentionally change subjects, locations or style.

When the action requires a specific starting state, use supported start-frame conditioning. A general reference guides appearance but does not guarantee the first frame. Match parameters to the chosen operation; derive framing from the input image when that operation has no ratio setting.

After generating a start frame, inspect the visible state needed for the action before buying its video. If it differs, correct the frame when the action is required; otherwise adapt the motion only when the brief permits. Check only relevant state, preserving user intent. If the state cannot be established, report uncertainty rather than marking it passed. This check concerns the actual image, not just its prompt; keep the observation and chosen correction with the run.

## Bind references before buying dependent media

For a continuing character or prop, use the supplied/selected identity image. Without one, the first usable scene frame can also be the reference; a separate paid anchor or character sheet is optional.

When supported, make later scene frames through reference editing with that image under the tool's accepted reference role. One edit creates one output and consumes one image call; it needs no preceding text-to-image call. Preserve the shared identity while describing the new scene's starting state and location. User-requested appearance changes override the named traits; backgrounds need not carry over. Scenes without shared identity, or with deliberately independent designs, need no common reference.

Write dependencies as supplied asset IDs or earlier step IDs, then resolve them to real files or Fish asset/object identifiers before actual calls. Two unrelated start frames do not establish a shared identity. Check that every required identity reaches its dependent scenes through actual supported inputs, rather than only the phrase "same character." Direct reference-video paths are also valid when supported and appropriate. If references are unavailable, state the limitation and choose a supported alternative within the brief and budget.

## Resolve sound and timing

For exact narration, use supplied speech or separate TTS unless native delivery of those words is verified. A script in the video prompt is not a verified speech track; do not invent narration parameters. Use one selected voice unless speakers intentionally differ. Silent and music-only requests need no narration generation.

Measure speech before committing to scene windows/clips when the script or total duration is strict. Adjust allocation within the requested total and supported durations; keep exact supplied text intact. If it cannot fit, report the conflict. Repeating identical synthesis or shifting its start does not resolve speech that exceeds its window. Rate/script changes require the brief's permission. Choose whether to retain or replace native audio.

## Assemble and inspect

Before dependent paid work, check supported operations/roles, resolved inputs, all preparation/edit attempts, timing and available assembly tools. Planned IDs and estimated durations are not existing files or measurements.

Assemble by scene index, using actual media geometry, measured audio and available processing. Preserve source files. Follow the [assembly guide](references/assembly.md) when combining clips/audio; subtitle timing needs measured alignment.

Check the complete film against story order, identity/state continuity, exact sound, duration and requested text. Frame samples and ASR are partial checks; disclose unviewed motion or unheard audio. Revise only affected media within authorized attempts, reassemble and recheck dependencies. Deliver the final film, actual prompts/input links/costs and unresolved defects; missing scenes or failed assembly are partial delivery.

Follow the [shared execution contract](../shared/core-skeleton.md) for paid execution and recovery.
