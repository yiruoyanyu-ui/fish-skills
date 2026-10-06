# Agent Connection and Platform Integration

## Two responsibilities

This repository provides a read-only stdio **Fish Skills MCP**. A separately authorized **Fish Audio MCP** executes media. The five API guides instead use REST examples and the API wallet. Reading a document is not running a generation pipeline.

See [quickstart](COLLEAGUE_QUICKSTART.md) for a ready-to-edit configuration.

## Backends

- **GitHub:** set FISH_SKILLS_BACKEND=github, FISH_SKILLS_GITHUB_REPOSITORY=yiruoyanyu-ui/fish-skills and FISH_SKILLS_CHANNEL=preview. Public reads can be anonymous. Private repositories require an authorized local gh login or FISH_SKILLS_GITHUB_TOKEN. Download redirects strip GitHub authorization when the host changes.
- **R2:** set FISH_SKILLS_BACKEND=r2 and configure R2_ACCOUNT_ID, R2_BUCKET, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY. Use a read-only bucket credential, not the publisher's write credential. FISH_SKILLS_PREFIX defaults fish-skills. No public bucket domain is required.
- **Local files:** build/publish to the default `.store/`, then run the stdio server. This is not an R2 upload.

```bash
uv sync --locked
uv run --locked fish-skills build
uv run --locked fish-skills publish dist/fish-skills-0.1.0-preview.3.zip --activate
uv run --locked fish-skills-mcp
```

The stdio server waits for client requests. It does not print documents interactively. Building requires committed Skill/config/review content.

## Task version and cache

Fetch the main instructions, retain the returned version, and use it for every reference read. The channel pointer caches for 60 seconds. Cached fixed content does not change when the channel advances. Corrupt/missing/unavailable content returns an error; the service does not silently substitute a different version.

Experimental status is a distribution label; consult the per-Skill evidence scope. It must not be interpreted as either "never tested" or "fully quality accepted".

## Fish API integration state

A separate platform-api development branch has implemented equivalent HTTP tools and passed local OAuth/R2 retrieval and one thermos execution chain. That branch is not deployed by publishing this repository. Existing online Fish connections are not guaranteed to expose these tools.

The reader returns ordinary dictionaries; an async platform handler must use an async storage adapter or a thread wrapper for blocking reads. Registration, account permissions, initialization, production bucket authorization and deployment require their own acceptance. Preserve Asset and Skill registrations when integrating both features.
