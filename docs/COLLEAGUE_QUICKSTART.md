# Colleague Quickstart

Start with the [validation inventory](VALIDATION.md), then inspect one [Skill](../skills/). The current English preview contains eight experimental entries with different evidence scopes. Case-tested means the listed case worked; it does not mean every use case or the translated revision has passed.

## Read the fixed release

```bash
git clone https://github.com/yiruoyanyu-ui/fish-skills.git
cd fish-skills
uv sync --locked
FISH_SKILLS_BACKEND=github \
FISH_SKILLS_GITHUB_REPOSITORY=yiruoyanyu-ui/fish-skills \
uv run --locked fish-skills read --version 0.1.0-preview.3 --skill product-photo-series
```

This is a public read. It needs no R2 credentials and makes no media request. Anonymous GitHub API rate limits may apply; use your own read-only GitHub token if needed, never the publisher's storage credentials.

## Connect a stdio MCP client

Replace the absolute directory. Add this entry without overwriting your existing Fish Audio/Asset connections:

```json
{
  "mcpServers": {
    "fish-skills": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/fish-skills", "run", "--locked", "fish-skills-mcp"],
      "env": {
        "FISH_SKILLS_BACKEND": "github",
        "FISH_SKILLS_GITHUB_REPOSITORY": "yiruoyanyu-ui/fish-skills",
        "FISH_SKILLS_CHANNEL": "preview"
      }
    }
  }
}
```

First request:

> List Fish Skills. Fetch product-photo-series from 0.1.0-preview.3 and its required references using that same version. Explain the inputs, tool sequence, authorization and quality checks. Do not generate media.

Tools: `list_skills`, `get_skill_instructions`, `get_skill_file`. References are resolved relative to the returned entry path; every follow-up file read pins the same version.

Actual media generation needs your own Fish Audio authorization, material and spending approval. REST API money and website/MCP credits are distinct. A successful local test-ledger reconciliation is not an online wallet invoice.

## Feedback

Open an Issue with Skill ID/version, expected behavior, observed behavior and an authorized, sanitized case. Do not upload keys, passwords, signed URLs or private customer material. Contribution uses a branch/PR. Only maintainers configure publication Secrets; readers do not need them.

Four unevaluated workflows have been withdrawn from the new catalog. Old immutable releases remain readable when explicitly pinned; default preview retrieval resolves the new reduced catalog.
