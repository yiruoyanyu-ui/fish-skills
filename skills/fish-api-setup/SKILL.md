---
name: fish-api-setup
description: |
  帮开发者配置并验证 Fish Audio API key，并讲清额度、限流、计费的坑。Use when 用户要接入
  Fish Audio API、调用返回 401/402/429、问"怎么拿 API key / 怎么查余额 / 为什么平台里有
  credits 却调不通"、或其他 fish-api-* 页面需要前置检查。先查已有 key 是否可用，可用则跳过；
  只在需要时才引导创建。读者=开发者（写代码调 API 的人）。
---

# Fish Audio API 接入（Setup）· v0.2

对标：ElevenLabs setup-api-key（先查已有 key → 验证 → 有效则跳过 → 无效才引导；安全纪律原样吸收）。
验证状态：端点、状态码、数字均为 2026-10-03 真 key 实测；可执行脚本 `examples/check_key.py`，整体回归 `evals/api-samples/run_all.sh`。

## 流程

### Step 0 · 先查已有 key（不问用户）
1. 环境变量 `FISH_API_KEY`；没有再查当前目录 `.env` 里的 `FISH_API_KEY=`。
2. **绝不打印、引用、回显 key**；需要提及时写"已配置（已脱敏）"。
3. 找到则运行 `python examples/check_key.py` 验证。有效 → 告知"Fish Audio 已配置可用"，问是否轮换，否则结束；无效 → Step 1。

### Step 1 · 引导获取 key
> 登录 fish.audio，进入开发者页（fish.audio/app/developers，这也是查看和充值 API 余额的页面）获取 API Key；创建入口的具体位置以网页为准，**创建后立即复制**。
> **不要把 key 贴进聊天**，写入本地 `.env`：
> ```
> FISH_API_KEY=your-api-key
> ```
> 已有该行则替换。保存后告诉我（不要发 key）。

### Step 2 · 验证并确认
以 `.env` 为准运行 check_key.py。成功 → "Done，key 有效，API 余额 X"；失败按下方状态码表处置。

## 验证 key（免费，不消耗额度）
```bash
curl -s https://api.fish.audio/wallet/self/api-credit -H "Authorization: Bearer $FISH_API_KEY"
# 200 → {"credit":"10.000000","cumulative_top_up":"10",...}    credit 即 API 钱包余额
# 401 → {"status":401,"message":"Invalid Token"}               key 无效
```
- **不要用 TTS 请求当验证**：余额为 0 时所有生成端点一律先返回 402，会掩盖参数错误。
- ⚠️ `/v1/user` 不存在（404），勿照搬 ElevenLabs 习惯。

## 状态码速查（实测）
| HTTP | 含义 | 处置 |
|---|---|---|
| 200 | 成功 | — |
| 400 | 参数错误。body `{"message": "...", "status": 400}`，message 直接指出哪个字段/取值不合法 | 照 message 改 |
| 401 | `{"status":401,"message":"Invalid Token"}`：key 无效 | 重新创建 key |
| 402 | key 有效但 **API 余额不足**（见下节） | 到开发者页充值 |
| 422 | 管理类端点（如 `POST /model`）缺字段，返回 `[{type, loc, msg}]` 列表 | 按 loc 补字段 |
| 429 | 并发超限："exceeded your current concurrency limit" | 降并发 / 排队重试 |
| curl 35 / HTTP 000 | 本地 TLS 握手失败（实测约 80 次调用出现 4 次，本机经代理出网） | 指数退避重试 2–3 次；不是服务端错误 |

## ⚠️ 额度独立：API 钱包 ≠ 平台 credits
所有生成端点在 API 余额为 0 时返回：
```
402 {"status":402,"message":"Insufficient API credit. API credit is managed independently from platform credit. Please visit https://fish.audio/app/developers to view your API credit balance or add funds."}
```
- **API 钱包与平台 credits（网页 / MCP 使用）完全隔离**：平台里有几百万 credits，API 钱包仍可为 0。
- 账号层面共享的是**音色库**（MCP 里克隆的音色在 `GET /model?self=true` 可见，实测），钱包不共享。
- 额度检查**先于参数校验**：余额为 0 时，无效 model、缺 text 都是 402。调试前先查余额。
- 401 vs 402：401 = key 无效；402 = key 有效但没钱。

## 并发上限
官方档位（按**累计充值额**，不必花完）：< $100 → 5；≥ $100 → 15；≥ $1000 → 50；企业定制。ASR 与其他接口共用同一并发池，**账号下所有 key 共享**；ASR 请求占槽直到返回，长音频可达数分钟。429 **不带 `Retry-After`**，自行指数退避。
响应头每次都带 `ratelimit-limit-concurrency`（本账号实测 5）与 `ratelimit-current-concurrency`。实测 8 路同时请求 → 5 个 200 + 3 个 429。上限随账户档位变化，以响应头为准；批量任务用信号量限流 + 429 退避。WebSocket 超限时服务端发 `{"event":"error","error":"Concurrency limit exceeded","max_concurrency":N}` 后关闭（取自源码定义，未实测）。

## 计费（实测）
- TTS 按输入文本 **UTF-8 字节** 计费：s2-pro **$15 / 百万字节**（600 字节扣 0.009；78 字节扣 0.00117，均与单价吻合）。中文每字 3 字节，一个汉字 ≈ $0.000045。
- **官方价目**（docs.fish.audio，2026-10-03 核对）：

  | 项目 | 价格 |
  |---|---|
  | TTS `s2.1-pro` / `s2-pro` / `s1` | $15 / 百万 UTF-8 字节 |
  | TTS `s2.1-pro-free` | $0（评估/原型，无 TTFA/DPA 保证） |
  | ASR `transcribe-1-pro` / `transcribe-1` | $0.36 / 音频小时，按秒向上取整，**错误请求不计费** |
  | 声音设计 `voice-design-1` | $0.01 / 次成功请求（一次返回多个候选也只计一次） |

  实测账单核对过的：s2-pro、s1、缺省头（均 $15/M）。ASR 与声音设计按官方价目，未逐项账单实测。
- 创建、查询、删除音色：实测未观察到扣费。
- **入账延迟**：扣费在调用后 5–35 秒才反映到余额（分批入账）。核对账单时先等余额稳定，不要调用后立刻查。

## 免费查询接口
- `GET /wallet/self/api-credit` → API 钱包（本页前文）。
- `GET /wallet/self/package` → **平台**订阅包（`type`、`total`、`balance`、`finished_at` 等，实测 200）。这是网页/MCP 用的那个额度，**不是**调 API 用的钱，别混。

## 接入方式：SDK 还是裸 REST
| 方式 | 安装 | 说明 |
|---|---|---|
| Python 官方 SDK | `pip install fish-audio-sdk`，代码里 `from fishaudio import FishAudio` | 包名≠导入名；自动读 `FISH_API_KEY`；实测 `client.tts.convert(text=..., model="s2.1-pro-free")`、`client.account.get_credits()` 可用 |
| JS/TS 官方 SDK | `npm install fish-audio`，`import { FishAudioClient } from "fish-audio"` | 模型是 `convert(req, backend)` 的**第二个位置参数** |
| 裸 REST / WebSocket | 无需安装 | curl、其他语言、边缘运行时；本系列 `fish-api-*` 页全部按这条写 |
- ⚠️ **同名陷阱**：PyPI 上的 `fishaudio`（作者 calcuis）和 npm 上的 `fish-audio-sdk`（无仓库）**不是官方包**，勿装。官方：PyPI `fish-audio-sdk`（仓库 fishaudio/fish-audio-python）、npm `fish-audio`（fishaudio/fish-audio-typescript）。
- SDK 的 ASR 默认参数与 REST 相反：`include_timestamps=True`（REST 是 `ignore_timestamps` 默认 true）；SDK 没有 ASR `model` 参数，要用 `RequestOptions(additional_headers={"model": "transcribe-1-pro"})`（实测加头后文本才带说话人标记）；且 SDK 的响应对象**丢弃 `speaker_turns` 与 `request_id`**，需要说话人分段就用裸 REST。
- 官方也提供 coding-agent skill：`npx skills add https://docs.fish.audio`（装 `fish-audio-sdk` 与 `fish-audio-api` 两个）。**与本系列的分工**：官方侧重"方法签名与请求格式"，本系列侧重"真 key 实测踩过的坑 + 钱包/计费/限流 + 可回归样例"。两者可同时装；冲突时以官方 OpenAPI（docs.fish.audio/api-reference/openapi.json）为准。

## 排障
每个响应都带 `x-fish-trace-id`，向支持反馈问题时附上它。

## 安全规则
- 永不让用户把 key 贴进聊天；永不打印 / 回显 key
- 持久配置优先 `.env` 或托管密钥，不写 shell 历史
- 浏览器 / 客户端应用：key 只放服务端，前端不得持有
- 测试用 key 建议限额，用完即轮换
