# Agent 安装与 Fish 平台集成

## 先连接两个入口

- **Fish Skills MCP**：本仓库实现，只读查询和获取 Skill 内容。
- **Fish Audio MCP**：现有媒体执行入口，继续用原有账号授权。

它们配合完成流程；无需把全部 Skill 本地安装后才能读取。当前是可运行的 stdio 分发服务，尚不是部署到 Fish 官方 MCP 的新增工具。

## 本地读取模式

在仓库执行 `uv sync --locked`、build、publish 到 `.store` 后运行：

```bash
uv run --locked fish-skills-mcp
```

它在 stdio 等待 MCP 客户端请求，不会在终端主动输出文档。

## GitHub Release 读取模式

设置 `FISH_SKILLS_BACKEND=github`、`FISH_SKILLS_GITHUB_REPOSITORY=yiruoyanyu-ui/fish-skills`、`FISH_SKILLS_CHANNEL=preview`。公开仓库可匿名读取，无需 R2 凭证。私有仓库需本机 gh 已登录，或在服务环境设置只读 `FISH_SKILLS_GITHUB_TOKEN`。实现不会把令牌写进下载 URL；跨域下载跳转不会携带 GitHub Authorization。

MCP 客户端配置示例（替换目录；客户端字段格式以实际配置为准）：

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

这是可填写的示例，不会由脚本自动覆盖现有客户端配置。连接后可让 Agent 执行：

> 查询 Fish Skills 目录，获取 product-photo-series 和同版本共享骨架及参考文件；说明执行步骤。先不生成媒体。

内容调用不产生 Fish 媒体 credits；GitHub、R2、运行环境本身是否产生费用取决于所用服务，不宣称零成本。

## R2 读取模式

设置 `FISH_SKILLS_BACKEND=r2`，再配置 R2_ACCOUNT_ID、R2_BUCKET、R2_ACCESS_KEY_ID、R2_SECRET_ACCESS_KEY；给 MCP **只读** bucket token，不能复用 CI 写入 token。FISH_SKILLS_PREFIX 默认 fish-skills。

客户端得到实际 version 后，每次 reference / 路由读取都传同一版本。最新频道指针缓存最多 60 秒，固定正文按版本缓存。存储不可用或校验失败时明确报错，不静默换内容；已缓存的固定版本仍可被该进程读取。

## 以后并入 Fish 官方 MCP

核心 `fish_skills.reader.SkillReader` 不依赖 FastMCP，三个方法返回普通 dict。platform-api 可以复用 reader，注册同名职责的 tools，并使用服务环境的只读存储配置。异步路由中通过 asyncio.to_thread 或项目的异步存储封装调用，避免阻塞。

需要另外完成平台仓库的工具 catalog/handler 注册、初始化路由说明、权限策略、客户端发现与部署验收。该工作不应伪装成“只把仓库 push 后官方 MCP 就有工具”；本版没有修改或发布 platform-api。
