# CI and R2 Setup

CI runs repository scripts when GitHub receives commits. It needs no separate server for packaging. Automatic validation and manual publication are separate.

## Workflows

- **Validate and package:** main push / PR validates committed Skill content and produces ZIP, manifest and checksums. Passing this job proves package structure, not creative quality.
- **Publish Skills:** manually run on main. Backend github creates a preview Release; backend r2 also uploads and reads back all content before switching the channel.
- **Switch R2 channel:** selects an existing matching-channel version, verifies it, then switches the pointer without overwriting content.

Publication and rollback share a concurrency group. Manual external writers must follow the same single-publisher discipline; there is no cross-publisher distributed lock.

## R2 credentials

Create a dedicated private bucket, normally fish-skills. Public GitHub source does not require making R2 public. Create a bucket-scoped Object Read & Write credential for CI and a separate Object Read credential for the MCP reader. Enter secrets directly into the provider/GitHub environment, not chat or source.

Repository → Settings → Secrets and variables → Actions:

| Type | Name | Meaning |
|---|---|---|
| Variable | R2_ACCOUNT_ID | Cloudflare account ID |
| Variable | R2_BUCKET | Bucket name |
| Variable | FISH_SKILLS_PREFIX | Optional; defaults fish-skills |
| Secret | R2_ACCESS_KEY_ID | Publishing access key ID |
| Secret | R2_SECRET_ACCESS_KEY | Publishing secret key |

Only maintainers need these settings. Colleagues reading public GitHub Releases do not need R2 credentials. Missing settings fail publication rather than silently skipping R2.

Objects live under fish-skills/releases/<version>/manifest.json and skills/...; channels/preview.json points to the active preview. Stable exists only after a separately reviewed stable release.

## Versioning, rollback and review

Increment the version for changed payload. A failed publication can retry the same unchanged commit; do not reuse a version for different content. Fixed versions reject replacement. Pointer activation follows full readback. R2 rollback verifies the complete previous version first; already pinned tasks keep their version.

GitHub mode discovers the latest published release in the channel and does not implement an R2 pointer rollback. Explicitly pin an old version when required. Historical withdrawn Skills remain available in immutable old releases; catalog removal is not a security revocation.

Stable publication requires reviews/<version>.json with version, payload content_digest, status=approved, reviewer and evidence links. A manually written approval cannot stand in for real execution/quality review. This English release remains preview.
