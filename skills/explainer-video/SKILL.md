---
status: dormant（2026-10-02 用户裁决：纯 MCP 无法达到成片及格线——缺逐 beat 动态片段的引擎工作流与装配服务；保留本页作为"Seedance 工作流暴露 + explainer 装配服务"两项平台需求证据与升级底稿。迷你版幻灯片级 demo 见 experiments/C04-mini-20261002）
name: explainer-video
description: |
  把一段科普/解说材料做成带旁白和字幕的解说短视频（图示驱动的合成片）。
  Trigger on: 解说视频、科普视频、讲解视频、explainer、把这段材料做成视频。
  Exclude: 实拍/出镜视频、UGC、纯旁白（用 narration 页）、音乐 MV。
  教学视角豁免：本页是"图解/剖面/示意"的**点名场景**（解说视频的正当形态），
  商品图与封面页的教学视角禁令在本页不适用，但仍禁无文字画面外标签烧字。
---

# 解说成片（Explainer Video）· v0.1（迷你版已验证 2026-10-02）

对标：Higgsfield video-explainer / faceless-*（22 风格 CMS 模板）+ BFL"生成与装配分离"。本页路线：**Fish 生成原子素材（旁白+图示帧），本地确定性装配**（ffmpeg）——与"全家桶模板"不同源，长处是可控与便宜，短处是风格库存为零。

## 结构公式（骨架的成片实例化）

```
解说材料 → 按"讲清一件事"切 beats（每 beat 一个独立概念）
→ 每 beat 一个教学画面（插画/示意，风格锚定一致）
→ 全文 TTS 旁白（narration 页能力）
→ 本地装配：画面时长对齐旁白 + 字幕烧录（punctuation 均分，声明近似）
→ QC：三看（看图是否符合 beat、看字幕对位、看成片时长）
```

## 流程要点

1. **beat 切分**：材料按概念切 2-4 段，每段一句话；不增删材料事实（解说版诚实律）。
2. **教学画面**：每 beat 一个 prompt；**风格锚定块逐字复用**（同一插画语言/色板/构图体系，三图协调）；文字只许出现在画面外（硬约束无文字照常适用——教学靠视觉隐喻不靠标签）。
3. **旁白**：narration 页（音色锁+表演标签可选）。
4. **装配（本地）**：旁白时长 → 按字数加权分摊到 beats → 逐段小视频各自裁音频 → concat；字幕烧录同 subtitles-burn 方法（均分，声明近似）。
5. **QC**：逐段抽帧目检（AI 有视觉时自检）+ 成片时长 ±0.5s + 字幕带位置。
6. **降级**：某 beat 画面失败 → 该 beat 用纯色+字幕过渡，交付说明，不冒充完整。

## 风格锚定块（本页首个实证：简洁平面插画）

"clean flat 2D illustration, warm sand and deep teal palette with one amber accent, thick clean outlines, generous negative space, no text"——新品类复制此模式：定义一次、逐字复用。
