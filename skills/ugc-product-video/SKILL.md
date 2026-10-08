---
name: ugc-product-video
description: |
  Create faceless, product-led promotional shorts with voice-over from real product references, including demonstrations, shot planning, generation and audio/video assembly when needed.
  Hands or POV may demonstrate use. Presenter, Avatar and real-person identity continuity use other workflows.
  Planning or script-only requests do not trigger generation. Purely silent displays and editing-only requests fall outside this complete workflow.
---

# UGC Product Video · v0.3-candidate.5

Start from real product references and deliver a complete short with supported product displays or usage demonstrations and narration. Native audio or separate-track assembly can achieve this goal. Hands or POV may assist; the faceless scope does not extend to Avatars or presenter-led explanations. Behavior and finished-media comparisons for this candidate remain incomplete.

## 1. Turn the product and goal into a script

Adopt existing requirements. For an ordinary short request with real product references, propose an overridable demonstration plan around known appearance and visible operations. Recommend duration, ratio, shots and voice from purpose, platform and language cues; briefly state chosen defaults when cues are absent. Do not fix every video at 10 seconds or three shots. Ask only for necessary materials, product facts or consequential choices that cannot reasonably be filled in, such as unknown internal structure essential to the requested operation. Deliver a plan or script when that is all the user requests.

Record product shape, parts, colors, visible surfaces, confirmed materials, real labels and visible mechanisms for use across shots. Preserve surface condition without manufacturing imperfections. Distinguish background annotations from product print; preparation must not automatically erase branding. Hidden sides and dimensions need additional evidence. Selling points need user-provided or confirmed information; marketing language is not verified efficacy.

Define the product feature or usage process the viewer should understand before selecting shots. "Introduce product → demonstrate one action → show result" is a starting option for a short demonstration. Shot count and order follow the goal and action. Record each shot's purpose, action, framing, visible product face, reference, estimated duration and narration. The action depicts the operation; narration explains it or a supported feature. Choose suitable actions to express confirmed selling points. Rewrite unsupported claims rather than generating an action to manufacture evidence. Keep cross-shot structure, lettering and color grounded in the same real reference; mark unseen parts unknown.

Short requests can use a compact shot table. Plan shots and copy before mapping tool parameters. Model duration options are not the creative structure.

Organize narration by shot purpose and check each product fact's source: real product information, explicit user-provided or confirmed information, or visible features in reference materials. A product photo supports appearance, visible components and readable labels, not inferred grip comfort, performance, durability, efficacy or discounts. A generated demonstration depicts an action; it does not validate the real product's performance, functions or efficacy. For example, generating an inverted cup without leakage does not prove that the product is leakproof. Such claims still need real product information or explicit user confirmation. Rewrite unsupported copy as visible features or operations. Separate creative descriptions from factual claims; "promotional" does not authorize invented offers or performance promises. Adjust copy by actual speaking speed and audio duration.

## 2. Choose the reference path

Check current Fish support for input roles, reference count, duration, ratio and audio before choosing production:

- **Multi-image / storyboard references:** Use a storyboard to express shot order only when explicitly supported. A four-panel board is optional. Layout follows shot count and input requirements; inspect product and action clarity.
- **Per-shot generation and assembly:** When storyboard references are unsupported or shot-level control is needed, use individual references and available editing tools. Explain extra materials, task count and cost first.

A complete collage is not a suitable first frame for an intended single-shot image. Use a single-shot keyframe for a first-frame path. Storyboard input does not guarantee exact cuts or timings. Verify actual input roles rather than mixing fields from different models.

Arrange targeted reference edits only when a specific structural, hand or action error affects subsequent generation. Editing attempts count toward the authorized limit. A vague "AI look" is not an automatic extra paid edit.

## 3. Generate and execute

Each video prompt describes shot action, spatial relationship, product features to retain and reference roles. Continuous multi-shot paths also state intended order and transitions. Check hand count and contact against the actual action. Branding, image text and subtitles follow the task. If the tool cannot accept the input combination, explain the gap and a feasible alternative.

Use the currently connected Fish environment. Models, voices, settings and prices follow current tools and estimates.

For paid execution, follow the [shared execution contract](../shared/core-skeleton.md). Budget only the materials, video, narration, editing and revisions actually needed for this task as one batch with attempt limits. Use applicable existing authorization.

## 4. Choose the audio path

Choose the audio path first. If the original already has narration whose copy, voice and action alignment satisfy the task, use the inspected original track directly; no extra TTS or track separation is needed. Consider separate-track assembly only when copy, voice or alignment needs independent adjustment, and check current editing support. Choose voice for the user's preference, language and expression.

When choosing separate-track assembly:

1. Save narration segments and their shot mapping, and measure each recording's actual duration.
2. Watch the generated video to establish real shot boundaries. Prefer an existing editing timeline. `ffmpeg` scene detection can assist, but reject false cuts from flashes or movement.
3. Align narration with relevant shots and actions. Shorten copy or adjust shots when audio is too long. If changing speed, listen for intelligibility and tone; no `atempo` value is a universally imperceptible threshold. Do not cut off a sentence.
4. Confirm original-track content. When new narration duplicates existing speech, replace or separate speech; lowering volume does not remove duplication. Retain ambient sound according to the task.
5. When choosing local assembly, read the [executable example](references/assembly-example.md) and use its helper or available editing tools. The helper's `keep/lower` modes require a confirmed zero relative start offset between source audio and video; otherwise normalize the timeline in an editor while preserving synchronization first. Protect raw footage and measure the last sentence. Adjust copy or shots when it overruns, and extend a frozen tail only when explicitly permitted. Choose subtitles according to the user.

## 5. Inspect, revise and deliver

Use available capabilities to inspect the complete video for product consistency, action/narration alignment, requested shots, plausible contact and hands, lettering and sound. N consecutive hard-cut shots normally have N−1 internal cuts; storyboard panel count is not observed shot count. Check long takes and transitions according to their actual structure. Duration tolerance follows the specific deliverable.

Mark viewing or listening checks that cannot be performed as incomplete; file creation does not replace them. Prepare dependencies only for the production path actually needed and disclose delivery or inspection gaps when capabilities are missing.

Target revisions at concrete defects within the batch budget and attempt allowance. If incomplete, deliver useful materials and specific gaps. A single demonstration shot or separate picture/narration files are not the requested finished video. New paid alternatives must follow current authorization.

Deliver video, source materials, script/shot plan, actual prompts/calls, model/parameters, costs and unresolved issues. Distinguish raw generation from postprocessed output. Save base results and status before processing so interruptions do not destroy deliverable work.
