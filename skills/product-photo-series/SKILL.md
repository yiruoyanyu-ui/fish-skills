---
name: product-photo-series
description: Make a coordinated square product photo series from a reference photo of drinkware or a thermos. Use for studio, tabletop and detail product images. Other product categories are outside the evaluated scope. Do not use for videos or general illustration.
---

# Product Photo Series

**Validation:** a thermos case completed reference cleanup and three scene edits on 2026-10-06, with output inspection and local test-ledger reconciliation. Tabletop and studio scenes were too similar. This is a case-tested preview, not evidence of general quality or exact geometry preservation. This English revision has not undergone a new Agent execution test.

The reference image anchors product identity; text specifies the scene.

## Required reading

Read `../shared/core-skeleton.md`, `references/dialect-gpt-image-2.json` and `references/category-thermos.md`. The shared skeleton owns authorization, execution, recovery and delivery; the category reference owns drinkware-specific constraints. Discover current models, parameters and prices from the execution service.

## Workflow

1. Confirm the product is drinkware or a thermos. For other categories, explain that this recipe has not been evaluated and stop this workflow.
2. Check missing content using the skeleton. Ask about reference, quantity, purpose or scene selection together, at most three questions. A missing reference is a blocker unless the user explicitly accepts text-only generation and its identity limitation.
3. Upload the user's reference using the currently available upload tool and its returned upload instructions. Retain the object key; do not publish signed URLs or credentials.
4. If the reference contains hands, surrounding text or a watermark, optionally generate one clean reference edit. Preserve product identity and use its output as the reference for subsequent scenes.
5. Write one final prompt per scene. Include "exactly the same product as in the reference" and an explicit lid state. Select scene, lighting and composition from the category reference, subject to the user's brief. Reference-guided generation still requires visual verification.
6. Estimate each scene separately with the exact workspace, model, inputs and parameters to be submitted. Follow the existing user authorization; use a distinct idempotency key per operation.
7. Submit once, poll the original generation ID to a terminal state, then retrieve the result and actual billing. A submission alone is not completion.
8. Check metadata, prompt constraints and available visual evidence. For drinkware, inspect steam, additional containers and lid state. Report checks that could not be performed.
9. Deliver outputs, final prompts, parameters, actual charges/refunds and decisions attributed to the user, defaults and constraints. Apply the skeleton's partial-delivery rules when a scene fails.
