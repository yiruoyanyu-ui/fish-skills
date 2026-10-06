---
name: fish-api-setup
description: Configure and check a Fish Audio REST API key, API wallet, concurrency and billing. Use before the other fish-api Skills or when debugging authentication and credit errors. For developers, not OAuth MCP setup.
---

# Fish Audio API Setup

**Evidence:** legacy notes report real-key tests on 2026-10-03. The old TTS page reports an eleven-case regression; its original run log has not been located for this release. These are reported historical observations, not a new validation of this English revision.

## Configure without exposing a key

1. Check whether `FISH_API_KEY` is already available without printing its value. Use `examples/check_key.py` from this Skill's directory to validate it.
2. If valid, reuse the configuration unless the user requests rotation. If absent or invalid, guide the user to the Fish developer area to create/configure a key privately.
3. Store keys in a secret manager or ignored local environment file. Never ask for a key in chat, write it to source, expose it in shell history or place it in a browser/client application.
4. Verify API wallet credit before any generation. The API wallet and website/MCP platform credits are separate. Voice identities may be shared by an account; that does not make the wallets interchangeable.

## Validation and errors

Use the key-check example rather than paid TTS as an authentication test. The historical check uses `GET /wallet/self/api-credit`; `GET /wallet/self/package` describes platform subscription credits, not API generation money.

| Result | Meaning / action |
|---|---|
| 200 | Authentication accepted; inspect the API balance separately |
| 401 | Invalid key; correct the configuration |
| 402 | Insufficient API credit; platform credits do not solve it |
| 400 / 422 | Inspect validation fields and correct the request |
| 429 | Concurrency/rate limit; limit concurrent requests and back off |
| TLS / connection failure | Diagnose transport; do not treat it as an invalid key |

Historical credit validation occurred before generation parameter validation. A zero balance may therefore mask an otherwise invalid generation request.

Read current `ratelimit-limit-concurrency` and `ratelimit-current-concurrency` headers rather than hardcoding account tiers. All keys of an account can share the same limit; long ASR occupies a slot until completion. A historical account had five slots, with an eight-request test yielding five successes and three 429s; that is not every account's limit.

## Billing and developer integration

Check current published pricing and the authorized budget before paid calls. Historical TTS observations billed UTF-8 input bytes rather than character count; ledger updates were delayed approximately 5–35 seconds. Historical ASR and voice-design price notes were not independently reconciled against bills. Do not convert those notes into current price guarantees.

These Skills use raw REST/WebSocket examples. The old notes also describe Python `fish-audio-sdk` (import `fishaudio`) and JS `fish-audio`; verify current official packages and interfaces before SDK work. For ASR, use raw REST when a particular SDK does not preserve speaker turns or request IDs.

Attach response request/trace IDs when reporting a problem, without attaching keys or private content. The samples are executable reference code, not automatically installed dependencies or permission to spend. Check each sample's requirements before execution.
