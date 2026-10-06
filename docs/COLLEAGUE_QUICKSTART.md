# 同事快速浏览与试用

## 先看什么

这是 Fish 媒体 Skill 的**公开预览仓库**，包括提示词规则、工作流、参考文件，以及按版本获取文档的只读 MCP。源码公开不代表已发布到 Fish 官方 MCP，也不代表所有工作流效果已验收。

建议先看三处：

1. [商品图工作流](../skills/product-photo-series/SKILL.md)：从饮器/保温杯参考图制作商品图系列。
2. [封面工作流](../skills/thumbnail-cover/SKILL.md)：封面制作及参考规则，当前能力边界见正文。
3. [媒体路由](../skills/fish-media-router/SKILL.md)：如何选择对应 Skill。

其余页面在 [skills/](../skills/)；状态以 [release.json](../release.json) 为准。当前发布包包含 12 个 Skill，其中 10 个 experimental、2 个 dormant。Dormant 是保留的历史文档，不作为可执行支持承诺。尚未发布的评测改动不包含在本轮公开版本。

## 下载并读取远端 Skill

需要 Git、Python 3.11+ 和 uv。只读试用不需要 R2 AK/SK，也不要求 GitHub 登录：

```bash
git clone https://github.com/yiruoyanyu-ui/fish-skills.git
cd fish-skills
uv sync --locked
FISH_SKILLS_BACKEND=github \
FISH_SKILLS_GITHUB_REPOSITORY=yiruoyanyu-ui/fish-skills \
uv run --locked fish-skills read --version 0.1.0-preview.2 --skill product-photo-series
```

该命令读取固定 Release 的 Markdown 和文件清单，不会生成图片。GitHub 的匿名 API 有限流；遇到限流时稍后再试，或由使用者配置自己的只读 GitHub token。

## 连接 Agent

在支持 stdio MCP 的客户端添加以下配置，替换绝对目录。不要覆盖已有的 Fish Audio / Asset MCP 配置：

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

先用这个请求确认读取：

> 列出 Fish Skills，获取 0.1.0-preview.2 的 product-photo-series，再读取其共享骨架和必需引用。说明工具调用顺序、输入要求、预算与质量检查。先不生成媒体。

三个工具分别是 `list_skills`、`get_skill_instructions` 和 `get_skill_file`。获取主文档后，后续引用固定同一个版本，避免任务中途混用新版规则。

实际生成还需单独连接 Fish Audio MCP，并使用自己的账户授权。Agent 按 Skill 调用已有报价、生成、状态查询工具；费用按实际操作产生。提供素材和支出授权后再提交生成任务。

## 当前验证到哪里

- 0.1.0-preview.2 发布包包含 12 个主文档、29 个 payload 文件；R2 上传及读回、独立 MCP 读取已验证。
- Fish API 的三个同职责工具已在独立开发分支通过本地 HTTP/OAuth 测试，尚未正式部署；不能期待现有线上连接自动出现这些工具。
- 一款保温杯走完清洗和三场景图片生成，共四张成功。credits 为隔离本地测试账本，不能作为线上钱包扣费证明。
- 图片基本约束有检查，但桌面图与棚拍图区分不足，产品结构精确一致性尚未验收；不能用单样本证明 Skill 普遍可靠或优于 HF。

## 怎么反馈与维护

浏览者可以开 Issue；修改通过分支与 PR 提交。反馈请包含 Skill ID、版本、期望、实际表现和脱敏案例，勿上传密钥、账户密码、签名 URL 或未获授权的素材。

作者修改 `skills/`，新增 Skill 同步 `release.json`；内容发版升版本，通过 CI 后发布 preview，质量评审后再考虑 stable。仅浏览和试用的同事不需要配置仓库 Secrets；R2 发布设置由维护者负责，见 [SETUP](SETUP.md)。
