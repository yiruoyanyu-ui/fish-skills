# Thumbnail Craft Reference

Adapted from earlier HF workflow research and local thumbnail experiments. This is a concept/prompt reference, not evidence that every framework has been evaluated. Execution and authorization belong to the shared skeleton.

## Concept selection

Develop at least three concepts: the image raises a question that the title/video answers. Select in this order:

1. Subject and emotion remain recognizable at approximately 120 pixels wide.
2. Product stays recognizable and intact. Cutaways/internal educational diagrams require an explicit brief.
3. Emotional contrast comes from the actual topic, not a generic fire/ice or orange/blue treatment. Temperature contrast belongs to temperature-related content.
4. There is a real curiosity gap, without inventing facts.

Default to human eye-level scale. Enlarge at most one real story element. The viewer should ask why something happened rather than whether the image is impossible. Avoid purple/cyan gradients, spark particles and excessive glowing outlines unless justified by the brief. One dominant saturated subject with subordinate background avoids competing focal points.

Sound/noise metaphors use readable lines or ripples interacting with the product, not explosion particles. Use photographic material words such as brushed metal, leather grain, fabric, seams and hinges. Do not falsely change the real product material. A floating-product concept may use a reflective surface if implied by the composition.

For an authorized unattended draft, use the current low-cost supported parameters and inspect recognition before spending on a final render. Two drafts are a limit, not permission to spend outside the user's approval.

## Sixteen concept frameworks

| # | Framework | Application |
|---|---|---|
| 1 | Before/after | Same subject in two contrasting states |
| 2 | Generic social UI | Unbranded chat/rating props; in-image words require authorization |
| 3 | Three-stage progression | Start → middle → result in three panels |
| 4 | Real screenshot | Prefer an actual frame when a source video is available |
| 5 | Staged portrait | Large subject, emotion, lighting; identity reference needed |
| 6 | Staged action | Freeze a suspenseful action without crowding the frame |
| 7 | Day-N badge | A truthful timeline badge; text policy still applies |
| 8 | Diagram | Explicit educational graphics; omit photographic lighting assumptions |
| 9 | Landscape | Environment leads, smaller subject on a third |
| 10 | Map/aerial | Map and truthful highlighted route or marker |
| 11 | Product | Product is the answer to the title's question |
| 12 | Added words | Deterministic annotation or continuation of the title |
| 13 | Repeated object | Many copies with a recognizable scale reference |
| 14 | Scale contrast | Large versus small, bounded by credibility |
| 15 | News strip | Generic short factual strip, no real station branding |
| 16 | Amplified reality | Enlarge one actual story element |

## Eleven prompt blocks

| Block | Content |
|---|---|
| Frame | Bold high-impact thumbnail, requested ratio, unified frame unless split is requested |
| Scene brief | Preserve supplied concrete content |
| Text | Default no text/readable labels/watermark; explicit text with exact lettering if requested |
| Subject | Dominant foreground subject, clearly separated, sharp; approximately 40–60% where appropriate |
| Key elements | Concrete topic-related prop/effect, only when justified |
| Logo | Only supplied/requested branding, preserving its intended shape and proportions |
| Location | Known place, time, weather and atmosphere |
| Composition | Thirds, depth and subject/background separation |
| Background | Support the subject with coherent color, texture, depth and edge treatment |
| Lighting | Concrete key/fill/rim sources; colored rim only when requested |
| Grade | Bright, clear impact unless the user requests a restrained treatment |

Do not let a generic background default contradict topic-specific concept selection. Historical defaults included landscape 16:9, one variant and an expressive subject; they are defaults, not mandatory aesthetics for every topic.

## Variants and reference analysis

Emotion options: shock, hype, fear, confusion, determination, smugness, charisma, disgust, awe, rage and laughter. Write specific eye/brow/mouth/head behavior rather than only an emotion label. Camera options: original design angle, low hero angle, close-up and wide slight Dutch angle. Submit requested variants individually, at most 16.

When a reference thumbnail is supplied, record brief, generic subject pose, elements, location, composition, background, split/count, person count and emotion details. Analyze it visually; do not automatically use it as generation input. A supplied identity photo for an authorized face match is a distinct input. Portrait identity remains unevaluated in this release.

## Targeted edits

Use the previous output as the image-edit reference. Change one target and restate invariants:

- Expression: change only expression; keep identity, structure, clothing, pose, scene and lighting.
- Background: replace only the background; preserve the subject and rebuild physically plausible light interaction.
- Background palette: recolor without changing scene structure or subject lighting.
- Rim light: change only the silhouette edge light.
- One prop: add/remove only the named object at the specified location.

These instructions do not guarantee unchanged pixels. Inspect actual results. After two failed edits of the same target, reassess the concept rather than grinding through more paid retries.

## Split layout

Use only when explicitly requested or present in the reference analysis. Two subjects imply halves; three or more can use vertical panels. Two confronting subjects in one scene do not automatically require a split.

Specify a split-frame image with N complete mini-scenes, bold seams and coherent grading. Add exactly one mode description: plain facets, before/after, equal-weight contenders or the user's custom panel brief. Default to no labels/captions/numbers between or inside panels unless explicitly authorized under the text policy.
