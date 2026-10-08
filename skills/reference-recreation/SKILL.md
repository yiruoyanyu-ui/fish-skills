---
name: reference-recreation
description: |
  Recreate a reference video, focusing on its actions, with the original or a replacement character.
  Use for motion transfer, dance reenactment and video action recreation; character images supply appearance while the video supplies movement.
  Analysis or prompt-only requests return text without generation. Still-image style matching and product photography use other workflows.
---

# Video Recreation · v0.2-candidate.5

Status: experimental. Motion fidelity has not been validated for this revision.

## 1. Use the supplied motion source

Adopt the user's video, stated interval, performer/replacement, duration and ratio. For a supplied clip with a clear target, proceed to capability checks and reference submission; the Agent need not first recognize every action or narrate the video.

Inspect the reference only when a decision requires it: choosing a span from a longer source, locating a performer, resolving unclear instructions or analyzing a reported deviation. Use available video/vision tools for that specific question. If unavailable or inconclusive, ask for the relevant timestamps or performer identification rather than inventing actions. A file path alone does not mean the Agent has visually inspected it; sampled frames cannot establish all continuous movement. Do not make unavailable Agent video understanding a blocker when the inputs and requested change are already clear.

Check file accessibility, duration and input compatibility through the available tools. Use the user's specified span and intended pace; record any processing. Without a motion video, state the gap; a screenshot is not a substitute.

When replacing a character, obtain their appearance reference and map them to the source performer. Retain the original performer when no replacement is requested and the tool supports that path. Camera, setting, clothing and sound follow this task; retaining an action does not require copying every scene feature.

## 2. Use a compatible motion-reference path

Check current capabilities in the session's selected Fish MCP. Verify that one request accepts the motion video and, when needed, the replacement appearance reference. For replacing only one of several performers, also verify selective mapping support; accepting multiple inputs alone does not establish this capability. Explain uncertainty before submission. Use actual input roles, such as `videoRef` and `ref`, and current length/ratio limits; these role names are examples, not universal fields.

A first-frame image or storyboard alone is not a motion-reference path. If no compatible path exists, explain the limitation and feasible alternatives before proceeding. Do not silently substitute ordinary text-to-video or image animation and call it action recreation. Do not add a preliminary identity image, storyboard or external service by default.

## 3. Draft the reference prompt from the user's request

Turn the user's request into a concise reference prompt: identify the motion source, map any replacement to the intended performer, and state which requested features to retain or change. Use supported controls for reference roles. Let the video carry movement detail; do not reconstruct every action in prose. Include camera, setting, clothing or sound instructions only when relevant to the user's request. Resolve contradictory instructions rather than adding more wording. If the user asks only for a prompt, return it without generating.

Example for a requested single-character replacement retaining camera movement:

```text
Use video 1 for the action sequence and camera movement. Replace its main performer with the character in image 1, using that image for appearance. Retain the reference action at its original speed.
```

This is an example, not a mandatory template. A good reference prompt makes the user's intended mapping and changes clear; it need not be long. Do not routinely add cinematic adjectives, invented choreography or second-by-second scripts. There is no separate prompt-enhancement step. Honor requested action adaptations without conflicting retention instructions. If an optional prompt adds no useful instruction, it may be omitted.

Follow the [shared execution contract](../shared/core-skeleton.md) for estimates, applicable authorization, attempt limits, fixed request identifiers and original-job queries. The contract's final-prompt step means the actual request here: when the tool permits omission, record "not supplied" rather than inventing a prompt. Record inputs, parameters and every attempt.

## 4. Compare actions and revise the cause

Use available inspection capability to compare the complete output against the selected source. Did the key action occur, in the requested order, with the intended performer? Check pace and requested camera/sound behavior. Compare corresponding events when durations differ. Sampled frames alone do not verify continuous motion or timing. If only frames or no visual inspection are available, disclose unchecked parts and leave motion acceptance pending for capable review; do not claim the Agent watched or verified the video.

When the user reports inconsistent motion, locate the differing action from their description or timestamps. Check the motion-reference input and character mapping. If needed, suggest a focused clip covering the key action's preparation and completion, and use a compatible generation duration. Explain any reduction from a requested full sequence before proceeding. Revise the specific ambiguity, compare the same event and keep retries within authorization; clipping is a candidate fix, not a guarantee.

Reference generation does not guarantee frame-exact choreography, cuts or identity. Verify a controllable path for strict timing and disclose limits. Deliver the video, source span, character mapping, actual request, costs and unresolved differences. Distinguish raw output from processing.
