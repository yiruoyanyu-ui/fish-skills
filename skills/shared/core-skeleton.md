# Shared Fish Media Execution Contract · v0.5-draft

This file covers paid execution, recovery and delivery. Creative plans, references, clarification, text, people, materials and colors follow the user's brief and the relevant Skill. Skills may read this entire file without filtering inherited visual rules. The filename remains compatible with existing links. Complete behavior acceptance across entrypoints is pending.

## Execution order

```text
Identify deliverable and necessary inputs → check current tool capabilities → plan and finalize prompt
→ estimate → apply authorization → submit → query original job → retrieve → inspect → deliver
```

Current Fish MCP responses define inputs, upload procedures, parameters, prices and states; do not duplicate interface manuals here. Complete necessary uploads before estimating the actual request. Paid preparation, generation and processing belong in the batch plan.

## Authorization

- Estimate before submitting, with the same workspace, model, inputs, prompt and price-affecting parameters. Re-estimate a changed request.
- Explain batch cost, count and attempt limit. Proceed under existing applicable authorization; obtain batch authorization when none applies.
- Sum multi-step estimates. Successful and failed attempts both consume the attempt allowance. Price changes within authorized spending and attempts may proceed; exceeding either requires additional authorization.
- Save a fixed request identifier using supported idempotency. Query the original request/job after an uncertain submission. A new identifier and resubmission are not recovery; do not automatically add paid attempts.

## Query and inspect

Save the original job ID, query to terminal status under the current contract, and retrieve results. Verify job success, file existence, task satisfaction and actual billing separately.

Visual/audio inspection follows the Skill and brief. Mark checks "not checked" or "cannot judge" when capability, sources or legibility are insufficient. Separate visible observations, aesthetic preference and unverified explanations. Job success and model scores do not replace artifact acceptance.

## Partial delivery and recovery

| Situation | Action |
|---|---|
| Required input missing or upload failed | Explain the gap and seek materials or an acceptable alternative. Do not promise reconstruction of unsupported objects or identities. |
| Estimate failed, unsupported capability or authorization exceeded | Pause paid execution and explain the cause and feasible options. |
| Submission timed out or status unclear | Query the original request/job; save state and ID. Report pending recovery when unresolved. |
| Generation failed or output inadequate | Retain record and actual cost. Explain targeted revisions within existing authorization and count their attempts; otherwise deliver the gap. |
| Processing failed or interrupted | Preserve base output before processing. Deliver available parts and incomplete items, without presenting base/separate materials as the complete deliverable. |

## Delivery record

Deliver results, purpose, actual prompt, reference roles, model/settings, job identifiers, all attempt states and actual costs. Distinguish user requirements from creative choices. Preserve raw and processed outputs. Mark unverified billing/refunds pending. Record durable asset identifiers/files rather than temporary upload credentials as long-term evidence.
