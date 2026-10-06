# Shared Media Execution Contract

This contract is shared by product photos, thumbnails and UGC. Changes affect all three workflows. Skill text is guidance; the current user's instructions and authorization take precedence.

## Workflow

Resolve missing content → upload references → optional cleanup → assemble the prompt → estimate → apply spending authorization → submit once with an idempotency key → poll the original ID → retrieve results and billing → inspect → deliver.

The Agent calls the connected execution tools directly. Do not assume another Agent inherits MCP authorization. If a tool or command is denied, do not loop on the same request. Use a permitted equivalent when available and disclose checks that remain unperformed.

## Missing information

| Missing item | Action |
|---|---|
| Reference, quantity, purpose or scene selection | Ask together, at most three concise questions with useful choices |
| Lighting, composition, material or style defaults | Resolve from the recipe and the actual reference; disclose defaults |
| Recipe constraints | Include applicable rules; keep category-specific restrictions in their category file |

Without a reference, unattended product generation stops unless the user explicitly accepts text-only fallback. Disclose that such generation cannot guarantee product identity.

## Spending authorization

Estimate using the exact workspace, model, inputs and parameters that will be submitted.

- For an interactive task without prior spending approval, show the estimate and obtain approval before submission.
- With existing explicit spending authorization, continue within its scope and limit. Explicit authorization without a budget cap is not an authorization to expand the requested deliverables.
- Without applicable authorization, do not submit.

Estimate scenes separately and explain unit prices and the expected total. If a new quote falls outside the approved scope, obtain the needed authorization. Report partial failures and charges separately. Never treat Skill retrieval as payment approval.

## Shared visual defaults

Default to no text, letters, numbers, logos or watermarks, except where the recipe's explicit text policy applies. Do not add objects, people, brands or copy that the request does not imply.

Do not promote a thermos-specific observation, such as "no steam", into a universal rule. A requested coffee scene may legitimately include steam. The recipe owns category restrictions; a model dialect translates them without inventing new ones.

## Quality checks

- Metadata: terminal status, output dimensions, files/hashes when available and charges/refunds.
- Prompt: requested constraints are present in the final submitted prompt.
- Pixels: inspect the actual output if vision is available; otherwise mark visual QC unperformed and request user review.

A successful generation status does not prove visual quality, product identity or user acceptance.

## Delivery and recovery

Provide outputs, final prompts, parameters, task IDs, charges/refunds and decisions identified as user input, resolved defaults or recipe constraints.

| Failure | Response |
|---|---|
| Missing unapproved reference | Report blocker and required material; do not generate |
| Upload failed | Report the failed step and object key; keep signed URLs in authorized private context |
| Quote failed or exceeded authorization | Stop before submission and explain |
| Generation slow or submission uncertain | Query the original ID or idempotency record; do not auto-submit again |
| One scene violates requirements | Deliver valid scenes and identify failed ones separately |
| Overlay, crop or assembly unfinished | Save the preliminary deliverable and base media first; deliver base output and processing script with unfinished status |
