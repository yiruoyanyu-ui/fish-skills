# CI 与 R2 设置

## CI 是什么

CI 是 GitHub 收到提交后替你运行脚本。配置已写在 `.github/workflows/`，仓库 push 后 GitHub 自动识别，不需要再找一台服务器运行它。

自动检查与手动发布分开：日常改文件看 Validate and package；准备发版才点 Publish Skills。

## 创建仓库与第一次运行

本仓库用于公开 Skill 预览和同事试用。公开源码与 Release 不需要访问授权；写入和发布仍需仓库权限。若另建团队内部仓库，可先设为 private，owner 按团队归属确定。

如果仓库尚未创建，在本项目目录运行，替换 OWNER：

```bash
gh repo create OWNER/fish-skills --private --source . --remote origin --push
```

仓库已存在则设置对应 remote 后 push main。不要向已有的不同项目强推覆盖。

打开仓库 Actions，确认 Validate and package 开始运行；成功后页面底部有 `fish-skills-package` 可下载。如组织关闭了 Actions，需要管理员启用；仓库设置为 `Settings → Actions → General`。

第一次发布无需 R2：Actions → Publish Skills → Run workflow → branch main → backend github。它会创建预览 Release，上传 ZIP、Manifest 和 checksums。私有仓库的读取者需要对应权限；不会因为创建 Release 就公开源码。

## 创建 R2 存储

登录指定 Cloudflare 账号 → R2 → 创建 bucket，建议专用 `fish-skills`。不要直接复用媒体素材 bucket 或更改其公开设置。MCP 通过 S3 API 读私有 bucket，不要求开启 r2.dev 公共访问。

R2 → Manage R2 API Tokens → 创建只针对该 bucket 的 Object Read & Write token 供发布；另建 Object Read token 供 MCP 服务。保存 Access Key ID、Secret Access Key、Account ID。**值直接填 GitHub Secrets / 服务环境，不贴聊天，不提交到 Git。**

[R2 官方鉴权说明](https://developers.cloudflare.com/r2/api/tokens/)；[boto3 官方接入示例](https://developers.cloudflare.com/r2/examples/aws/boto3/)。创建 bucket、开通 R2 或取得授权需要在有权限的账号下进行。

## GitHub 要填哪些配置

仓库 → Settings → Secrets and variables → Actions：

| 页签 | 名称 | 内容 |
|---|---|---|
| Variables | `R2_ACCOUNT_ID` | Cloudflare Account ID |
| Variables | `R2_BUCKET` | bucket 名称 |
| Variables | `FISH_SKILLS_PREFIX` | 可不填，默认 `fish-skills` |
| Secrets | `R2_ACCESS_KEY_ID` | 发布 token 的 Access Key ID |
| Secrets | `R2_SECRET_ACCESS_KEY` | 发布 token 的 Secret Access Key |

配置后 Actions → Publish Skills → backend r2。缺项会失败，不会悄悄跳过 R2。现有 GitHub 预览版可在同一 commit 再次触发 r2 发布，不需重复改源码。

私有包不能仅依赖公开域名保护。这里不创建公共写入接口，发布权限由仓库写权限及 bucket token 管理。[GitHub Secrets 官方说明](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)。

## R2 中实际长什么样

```text
fish-skills/
  releases/0.1.0-preview.2/
    manifest.json
    skills/product-photo-series/SKILL.md
    skills/shared/core-skeleton.md
    skills/...
  channels/preview.json
  channels/stable.json     # 首个稳定版通过评审并发布后才存在
```

版本内保存全部 Skill 和引用文件，整个任务固定同一包版本。Manifest 包含文件大小/hash、源码 commit、每个 Skill 的描述和状态。预览版指针与稳定版分开。

上传采用条件写入，同版本不同内容拒绝覆盖；上传后全部读回校验成功才切换频道。CI 并发串行化；目前没有跨其他发布者的分布式锁，手动脚本不得与 CI 并发发布。

## 更新和回退

新内容必须升版并提交。R2 回退：Actions → Switch R2 channel → 已有旧版本 → 对应 channel；脚本重新检查全部文件，不删除新版。任务已取回固定版本的继续原版，新任务在指针缓存刷新后采用旧版。

GitHub 模式只是过渡发放后端，没有可写的频道指针；需要回退时让 Agent 指定旧版本。不能宣称它支持与 R2 相同的回退语义。

稳定版先整理实际评审证据，再设置 channel=stable 并填写 `reviews/<version>.json`，格式：

```json
{
  "version": "0.1.0",
  "content_digest": "<对应全部 payload 文件清单的摘要>",
  "status": "approved",
  "reviewer": "<负责评审的人>",
  "evidence": ["<评审报告链接或可追溯文件>"]
}
```

版本写入 release.json 后可先保持 preview 打包获取 content_digest，再整理评审、切换 stable 并提交。两者 payload 不变时摘要不变。不能为了让流水线通过伪造 approved 或证据。
