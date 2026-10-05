# 封面工艺参考 · 16 框架 + 11 块结构 + 情绪/机位档 · v0.1

> 蒸馏自 Higgsfield thumbnail-generation（App 2.1.0，2026-10-01 全文读毕）。本文件是工艺知识，不含流程与门禁（在 SKILL.md 与骨架）。

## A. 概念层：16 框架（先选"画什么"）

**信息差原则**：封面必须打开一个信息差——图提出问题，标题/视频回答。动笔前脑暴 ≥3 概念（可组合框架），选最强。**诚实律**：可夸张、不可歪曲视频内容。

**择强判据（2026-10-02 首轮实败驱动，按序筛）**：①一秒可读：120px 宽下一眼认出"这是什么、什么情绪"；②产品完整可辨：**默认不切开、不拆解产品**——剖面/图示/解构图（框架 8 类）只在用户点名要"教学图示"时用，因为它牺牲"这是什么"换取"为什么"（首轮实证：剖面概念输在产品不可辨）；③有情绪对比：画面要有可感知的情绪张力；**"温度"类对比只属于卖点是温度的产品（保温杯/冷饮等）**——其他主题禁止默认套用冷暖色温套路（2026-10-02 TT1 实证：降噪耳机被画成橙蓝冰火两重天，因判据③曾被保温杯反馈以字面"温度"表述，被跨品类误用）；视觉语言必须从**主题自身语义**选取（噪音→安静可以是"混乱锯齿→平直细线"，不必是火与冰）；④信息差。四条全过才算最强，冲突时①优先。
**反俗套条款（与放大上限同层）**：橙蓝撞色、紫青渐变、火花粒子是 AI 封面三大俗套；概念阶段的"情绪对比"应优先用主题专属的视觉隐喻（降噪=声波湮灭、防水=水珠弹跳、快充=电弧入电池），俗套配色只在无更贴题方案时作底。

**能量可视化与饱和度纪律（2026-10-02 三联交叉验证后补）**：声波/光束/电弧/信号等能量元素一律**摄影级语言**——半透明体积感、自然发光、贴近真实物理形态的纹理（声波=有起伏衰减的波纹，**不是平行几何直线**）。全图只允许**一个**高饱和主角色，背景与辅助元素保持低饱和，禁止双高饱和对撞（实证用户语："色差似乎弄的有点太显了"）。poster-grade ≠ 平面图形风：非框架 8 时保持摄影真实感，禁止 "clean and graphic" 式霓虹几何线进入非图形框架的 Style 块。

**产品互动与材质纪律（2026-10-02 终局视觉对照补，AI 目检双侧成片后定位）**：
- **声音/波类 = 波形线条语义**：进入侧尖锐杂乱 → 产品处转换 → 离开侧平直优雅细线，动线**横穿画面与产品互动**（产品=动线上的转换器）；**禁**"撞上产品碎裂成粒子"（粒子=爆炸烟尘语义，实证画出烟雾团而非声波）。声波的可读形态是**线与波纹**，不是团块。
- **材质写"能摸到"的词**：真皮纹理/拉丝金属/织物/缝线/铰链五金；**禁 plastic**（除非用户点名塑料产品）——一词之差渲染掉一档（实证：plastic→CGI 光滑感 vs leather/metal→产品摄影质感）。
- 悬浮产品默认配 glossy surface + soft reflection（反射面提档次）。
- 动线占满横幅形成连续性，禁"半边能量半边空"的对分构图。

**放大上限（2026-10-02 二轮实证补入）**：框架 16 放大现实的原律——只放大**一件**真实存在于故事里的元素，保持可信；环境级的超现实布景（冰墙火墙夹击类）即属过度放大，毁可信度。用户评语"有点夸张了"即踩此线。判定法：把画面描述给一个没看过视频的人，若对方反应是"真会有这画面吗"而非"我想知道为什么"→超限。

**视角尺度门禁（2026-10-02 保留题实证补入）**：封面默认**人眼尺度**——站在地上一眼能看到的画面（HF 对照组同题获胜的正是地面视角）。太空视角/剖面/微距宇宙/内部结构等"教学视角"与框架 8 同类：牺牲"这是什么"换"为什么"，**仅当用户点名要教学图示时才用**（保留题实败：太空视角的金光砸地球，用户"不知道什么意思"）。
**概念草稿门禁（流程新增）**：无人值守时**先出 1K/low 草稿**（最低档），宿主有视觉则以"外行测试"自检草稿——一个没看过视频的人扫一眼能否说出"这是什么、想知道什么"；自检不过→换概念再出草稿（最多 2 轮），通过才升成片档位。交互模式则把概念一句话+草稿给用户挑。

| # | 框架 | 实现要点 |
|---|---|---|
| 1 | 前后对比 | 分屏（split frame）：同一主体两态，最大反差 |
| 2 | 社交 UI | 通用聊天气泡/评分卡道具（不碰真品牌）；内嵌文字需显式授权 |
| 3 | 三段进程 | 3 竖panel：起点→中段→结果 |
| 4 | 真实截图 | 非生成——用视频真实帧（有源片时优先提示用户） |
| 5 | 摆拍肖像 | 默认框架：主体大+情绪+布光；背景极简（人像需人脸锁定） |
| 6 | 摆拍动作 | 定格一个"正在进行"的悬念动作，画面不拥挤 |
| 7 | 第 N 天徽章 | 任意框架+DAY N 徽章（内嵌字需授权；选弧线后 20% 的天数） |
| 8 | 图形示意 | 非写实：干净图示/曲线/图表，撤 photoreal 与布光块 |
| 9 | 景观 | 环境为主角，主体小、放三分线 |
| 10 | 地图/航拍 | 地图框+高亮路线/圆圈标记 |
| 11 | 产品 | **产品即主角**（商品图链路直接复用）；信息差=产品是标题问题的答案 |
| 12 | 加字 | 叠字作标注（箭头+词）或作标题问题的续答 |
| 13 | 物体重复 | 大量同一物体铺满画面+一个比例参照 |
| 14 | 尺寸差 | 巨大 vs 微小的极端比例对比 |
| 15 | 新闻字幕条 | 通用"breaking news"条（内嵌字需授权；短、真实、无真台标） |
| 16 | 放大现实 | 真实故事元素放大一件（KEY ELEMENTS oversized），过度即失真 |

## B. 渲染层：11 块提示词结构（按序装配）

| 块 | 内容 | 取舍 |
|---|---|---|
| 1 帧合同 | "Bold, punchy YouTube-thumbnail composite — poster-grade, high-impact, NOT a muted cinematic still, 16:9 aspect ratio, single unified frame — no split-screen, no diagonal divide" | 恒含（split/图形框架除外） |
| 2 场景简报 | SCENE BRIEF (must be depicted exactly): <用户原文> | 用户给了具体内容才加 |
| 3 文字合同 | 默认 "No text, no readable UI labels, no watermark."；显式烧字才用 TEXT 块（逐字内容+超大无衬线+描边/发光+不遮脸） | 恒含其一 |
| 4 主体 | 大而主导（占画面 40-60%，胸像/中近景，前景，与背景强分离），结尾 "crisply sharp" | 有主体恒含 |
| 5 关键道具 | 让画面 pop 的标志性道具/效果；默认=主题最具体的名词、超大、飞向镜头 | 有则加 |
| 6 logo | 2D 原样置入（形/色/比例不动）或 3D 渲染体 | 有才加 |
| 7 地点 | 地点/时间/天气/氛围 | 知道才加 |
| 8 构图 | 三分线、景深层次、主体-背景分离 | 恒含 |
| 9 背景处理 | 高饱和色场/渐变/高对比/纹理/虚化/边缘衰减，混融不分割 | 恒含 |
| 10 布光 | 三灯位 rig（主光塑形+柔光补+轮廓/发丝光分离背景）；彩色轮廓光只有用户点名才用 | 有人像恒含；纯静物可从简 |
| 11 调色 | vivid high-impact grade, punchy contrast, bright exposure, poster-punchy | 恒含（用户要素净才降档） |

**每字段默认值**（用户与参考图都没给时）：比例 16:9；变体 1；情绪 shock（有人时）；背景=高饱和撞色渐变+暗角；构图=主体大居三分。

## C. 情绪档 × 机位档（变体=两者组合，上限 16）

情绪 11 档（括号=写进 prompt 的具体描述）：shock（张嘴倒吸、瞪眼）/ hype（狂喜）/ fear（僵住）/ confusion（挑眉）/ determination（咬紧、激光专注）/ smug（得意坏笑）/ charisma（沉稳磁感）/ disgust（后仰皱脸）/ awe（下巴掉落）/ rage（咬牙怒视）/ laugh（仰头）。
机位 3 档：Take1=设计机位原样；Take2=低角度英雄视角；Take3=极近特写怼脸（背景压成散景）；Take4=广角微荷兰角、环境更多。

## D. 参考封面分析合同（用户给示例图时）

用自己的视觉抽 STRICT JSON：brief / subject（姿态泛写，不写具体人）/ elements / location / composition / background / split(bool) / split_count / person_count(0-3) / emotion(11 档或 other) / emotion_detail（一句：眼/眉/嘴/头角）。
**参考图只经眼睛分析，绝不作为生成输入**（除非用户要 Match 人脸→走人脸锁定）。

## E. 精修词库（i2i 手术刀 · 2026-10-02 补，源自对标+按 gpt-image-2 方言改写）

调用：`generate_image_edit`，ref=上一张成品；**每轮重申不变项**（骨架迭代纪律）。五段模板，只换尖括号：

1. **换表情**（有人时）：`Change ONLY the person's facial expression to: <情绪短语>. Keep identity, face structure, hair, pose, body, clothing, background, lighting and composition EXACTLY unchanged, pixel-faithful — pure expression swap.`
2. **换背景**：`Replace ONLY the background with: <新背景描述>. Keep the subject and all foreground elements EXACTLY unchanged. Rebuild the lighting wrap around the subject so the new background's light direction and color read naturally.`
3. **背景重上色**：`Shift ONLY the background color palette to dominant <色系> tones. Keep the background's structure, content and depth exactly — only recolor. Keep the light on the subject unchanged.`
4. **换轮廓光**：`Change ONLY the rim light on the subject to <短语> — the bright edge tracing the silhouette. Do NOT change key light, background, pose or composition.`
5. **加/去一件道具**（我们补）：`Add ONLY <物件> at <位置>. / Remove ONLY <物件>. Keep everything else EXACTLY unchanged, pixel-faithful.`

链式规则：每次精修的输出作为下一次输入；连续同一处失败 2 次 → 换概念重渲染，不道歉式硬磨。

## F. 分屏合同（4 模式 · 源自对标）

**触发**：用户明确要分格布局（split/before-after/versus/side by side/左右对比）才触发；画面里"两物对峙"不算分屏（那是统一画面）。参考图分析 split=true 同样触发。
**格数**：按点名对象数定 N；N=2 → 对半 halves；N≥3 → 竖条 vertical panels。
**替换句**（替代 11 块结构的块 1）：`SPLIT-FRAME thumbnail, 16:9: the frame divided into N [halves|vertical panels] by clean bold seams, each panel its own complete mini-scene, unified premium grade across all panels.`
**模式句（追加且只追加一句）**：
- plain：`Each panel shows one facet of the story: <格1: …; 格2: …>.`
- before/after：`LEFT panel: the BEFORE state — <…>. RIGHT panel: the AFTER state — <…>. Maximum visual contrast between the two states.`
- versus：`Each panel presents one contender lit and framed like a fighter poster: <…>. Equal visual weight, confrontation energy across the seam.`
- custom：用户逐格描述原样进。
**恒定收尾**：`No labels, no captions, no words, no numbers on or between the panels — the comparison reads purely visually. All panels graded as one premium image.`（格内格间禁一切文字，对比纯靠画面——120px 哲学）
