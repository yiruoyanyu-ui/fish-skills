---
name: thumbnail-cover
description: Create or edit a video/content thumbnail in landscape, portrait or square format. Use when the user requests an actual cover image. Analysis and title suggestions do not trigger generation. Existing tests cover limited concepts; portrait identity and general quality remain unverified.
---

# Thumbnail / Cover

**Validation:** earlier real image comparisons exist, with limited concept coverage and remaining factual-review and independent-review gaps. Do not label the complete workflow quality-approved. This English revision has not undergone a new Agent execution test.

Read `../shared/core-skeleton.md`, `references/dialect-gpt-image-2.json` and `references/thumbnail-craft.md` before execution.

## Thumbnail-specific rules

- Default to a clean text-free render and a deterministic text overlay afterward. A requested title is not permission to render its lettering inside the generated image. Use in-image text only when explicitly requested; specify exact text and typography.
- Develop at least three concepts using the framework reference. The image opens a question that the title/video answers. Exaggeration must not misrepresent the actual content.
- Deliver the concept candidates, framework numbers, selection and rejection reasons. For abstract mechanisms, use elements from the real topic's scene. Do not default to body organs or purple/cyan neon metaphors.
- At approximately 120 pixels wide, the subject and intended emotion should remain legible. If visual inspection is unavailable, mark this check unperformed.

## Workflow

1. Confirm that image creation or editing is requested. For review or title advice, respond in text without a generation call.
2. Resolve topic, aspect ratio, text policy and number of variants. Defaults: landscape 16:9 and one image. If variants are requested, use emotion/camera combinations, at most 16, submitted individually rather than as an opaque count batch.
3. If a concept contains a person without an identity reference, clarify once whether the user will supply a reference, accepts a synthetic person or prefers no person. Disclose that portrait identity has not been validated.
4. Develop at least three concepts and select using legibility, recognizable subject, topic-specific emotional contrast and curiosity gap. Default to eye-level scale; internal/cutaway/educational views require an explicit brief.
5. Where authorized, generate a low-cost draft using currently supported parameters. Inspect whether a viewer can recognize the subject and the question. For unattended execution, allow at most two concept drafts within the authorized budget; for interactive execution, show the concept and draft for selection. Do not assume that an estimate authorizes extra drafts.
6. Assemble the eleven prompt blocks in the craft reference. Follow the shared estimate/authorization/submit/poll/result/QC workflow. Add the 120-pixel check and any deterministic overlay.
7. For small edits, use the previous output as reference and change one target at a time. Restate what must remain unchanged; verify the output rather than treating "pixel-faithful" wording as a guarantee.
8. Deliver the chosen concept, framework, candidates, final prompt, output, overlay file if applicable, costs and limitations. Save a preliminary deliverable before post-processing. If text processing fails, provide the clean render and script with its unfinished status.
