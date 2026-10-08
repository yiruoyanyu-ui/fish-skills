---
name: ugc-product-video
description: |
  Create faceless, product-led promotional shorts with voice-over from real product references, including demonstrations, shot planning, generation and audio/video assembly.
  Hands or POV may demonstrate use. Presenter, Avatar and real-person identity continuity use other workflows.
  Planning or script-only requests do not trigger generation. Silent displays and editing existing footage do not require this complete workflow.
---

# UGC Product Video · v0.3-candidate.4

Status: experimental. Use concrete demonstrations and segmented narration with the product as the protagonist. Historical Fish evidence covered one 10-second path, not presenter-led UGC or every format. Recent comparisons and independent text checks found product-fidelity and unsupported-claim failures; this candidate is not quality-approved.

This candidate adds sentence-level narration source checks. The local assembly helper checks video/audio track durations and publishes completed files atomically. Behavior and artifact acceptance remain incomplete. The English adaptation has not undergone a new behavior or media comparison.

## 1. Turn the product and goal into a script

Extract product references, audience, purpose, duration, ratio, language, narration and sound preferences. Ask only consequential missing choices; adopt existing requirements. Photographic and editing details may use proposed defaults. Deliver a script when requested; obtain needed materials or goals before making a complete video.

Record visible product shape, parts, colors, surface appearance, real labels and demonstrated mechanisms for use across shots. Preserve surface condition without manufacturing imperfections. Distinguish background annotations from product print; preparation must not automatically erase branding. Hidden sides and dimensions need additional evidence. Selling points need user-provided or confirmed information; marketing language is not verified efficacy.

Define what process and benefit the viewer should see before selecting shots. "Introduce product → demonstrate one action → show result" is a starting option, not a mandatory pattern. Shot count, people and order follow the goal and action. Record each shot's purpose, action, framing, visible product face, source, estimated duration and narration. Purpose defines what to communicate, action provides visible evidence, and narration explains that action or supported features. Change the action or copy when the demonstration cannot support a claim. Keep cross-shot structure, lettering and color grounded in the same reference; mark unseen parts unknown.

Read [creative planning](../shared/creative-planning.md) for complex plans; short requests can use a compact shot table. Plan shots and copy before mapping tool parameters. Model duration options are not the creative structure.

Segment narration by shot purpose. After writing, check each sentence's basis: user-provided facts, visible material or what the video actually demonstrates. A product photo supports appearance, visible components and readable labels, not inferred grip comfort, performance, durability, efficacy or discounts. Explicit user-provided facts may be used with their source recorded. Rewrite unsupported claims as observable features or actions, asking only if the missing fact materially affects the plan. Separate creative descriptions from factual claims; "promotional" does not authorize invented offers or performance promises. Adjust copy by actual speaking speed and recorded duration, not a universal character count.

## 2. Choose the reference path

Check current Fish support for input roles, reference count, duration, ratio and audio before choosing production:

- **Multi-image / storyboard references:** Use a storyboard to express shot order only when explicitly supported. A four-panel board is optional. Layout follows shot count and input requirements; inspect product and action clarity.
- **Per-shot generation and assembly:** When storyboard references are unsupported or shot-level control is needed, use individual references and available editing tools. Explain extra materials, task count and cost first.

A complete collage is not a suitable first frame for an intended single-shot image. Use a single-shot keyframe for a first-frame path. Storyboard input does not guarantee exact cuts or timings. Verify actual input roles rather than mixing fields from different models.

Prepare references only when a specific structural, hand or action error affects subsequent generation. Editing attempts count toward the authorized limit. A vague "AI look" is not an automatic extra paid edit.

## 3. Generate and execute

Each video prompt describes shot action, spatial relationship, product features to retain and reference roles. Continuous multi-shot paths also state intended order and transitions. Check hand count and contact against the actual action. Branding, image text and subtitles follow the task. If the tool cannot accept the input combination, explain the gap and a feasible alternative.

Use the currently connected Fish environment. Do not infer a platform from budget units or switch to production/external services by default. Models, voices, settings and prices follow current tools and estimates. Internal narration is a video dependency, not a restored standalone audio Skill.

Follow the [shared execution contract](../shared/core-skeleton.md) for spending, idempotency, original-job queries, inspection disclosure and delivery. Budget preparation, video, narration, editing and revisions as one batch with attempt limits. Use applicable existing authorization. Query the original job after failure or an uncertain submission. Shared dependency changes have not passed complete behavior and artifact acceptance.

## 4. Segmented narration and audio/video assembly

Consider separate tracks when copy or voice needs independent editing. Check whether native audio supports later changes. Choose voice for the user's preference, language and expression; briefly state an unspecified default.

1. Save narration segments and their shot mapping, and measure each recording's actual duration.
2. Watch the generated video to establish real shot boundaries. Prefer an existing editing timeline. `ffmpeg` scene detection can assist, but reject false cuts from flashes or movement.
3. Align narration with relevant shots and actions. Shorten copy or adjust shots when audio is too long. If changing speed, listen for intelligibility and tone; no `atempo` value is a universally imperceptible threshold. Do not cut off a sentence.
4. Listen to original audio. Keep it if it already satisfies the brief. When new narration duplicates existing speech, replace or separate speech; merely lowering volume does not remove duplication. Retain ambient sound according to the task.
5. For local assembly, read the [executable example](references/assembly-example.md) and use its helper or available editing tools. Protect raw footage, measure the last sentence and final duration, and adjust copy/shots before overrunning. Freeze the tail only when explicitly permitted. Subtitles are optional and user choices override defaults. Watch and listen to the assembled output; file creation alone is not acceptance.

## 5. Inspect, revise and deliver

Watch the complete video for product consistency, action/narration alignment, requested shots, plausible contact and hands, lettering and sound. N consecutive hard-cut shots normally have N−1 internal cuts; storyboard panel count is not observed shot count. Check long takes and transitions according to their actual structure. Duration tolerance follows the specific deliverable, not a universal ±0.3 seconds.

Use available inspection tools. Disclose missing checks when a tool is unavailable instead of pointless environment probing or repeated installations. Listen when possible; otherwise explicitly leave audio review pending rather than claiming acceptance.

Target revisions at concrete defects within the batch budget and attempt allowance. If incomplete, deliver useful materials and specific gaps. A single demonstration shot or separate picture/narration files are not the requested finished video. New paid alternatives must follow current authorization.

Deliver video, source materials, script/shot plan, actual prompts/calls, model/parameters, costs and unresolved issues. Distinguish raw generation from postprocessed output. Save base results and status before processing so interruptions do not destroy deliverable work.
