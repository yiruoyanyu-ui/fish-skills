---
name: product-photo-series
description: |
  Create studio, usage-scene, detail or coordinated commercial product images from product references, or edit existing product photos.
  Use for product photography, ecommerce hero images, contextual shots and detail close-ups. Planning or critique alone does not trigger generation.
  Real-product fidelity requires reference photos; text-only briefs must explicitly accept concept images rather than exact reconstruction.
---

# Commercial Product Photography · v0.4-candidate.6

Status: experimental candidate. Behavior and artifact acceptance remain pending.

Use references as the source of product appearance. Vary scene, viewpoint, lighting and distance to serve different image purposes. References help fidelity, but outputs still require inspection.

## 1. Define the deliverable and materials

Use the existing brief to establish where the image will appear, what it should communicate, image count and aspect ratio before choosing each scene. A single-image request stays a single image; square output is not mandatory.

Treat these choices independently. Studio photography does not imply no people, and a usage scene does not imply a handheld product.

| Choice | Decision basis |
|---|---|
| Use | Hero images prioritize recognition; details explain; ads attract attention and accommodate information. Adopt the user's platform and layout requirements. |
| Image type | Studio shots show form; contextual shots show environment or use; details explain a component. Combine them for the task rather than requiring a three-image package. |
| People | No person, hands, partial person or model, depending on scale, operation, wearing or brand expression. Keep the product recognizable. |
| Visual direction | Choose clean, dramatic, warm, vivid or another direction for the product and purpose. "Premium" does not automatically mean dark, unoccupied or minimal. |

### When to ask and when to decide

- Reuse stated hero/scene, people, ratio and style requirements without asking again. The Agent handles exposure, light placement and depth of field; the user need not know photographic terminology.
- For "make a product image series," offer a short recommendation and ask the most consequential choice when purpose or people materially change delivery. For example: "I suggest a hero, usage scene and detail. Would you prefer product placement in a setting or a handheld demonstration?" Explain how each helps show this product's use or scale; the user may also delegate the choice.
- If the user says "you decide," "just make it" or "don't ask," state the plan briefly and proceed. Without purpose clues, begin with clear overall appearance; give each image in a set a different job.
- Recommendations remain overridable. Unspecified settings are creative choices, not product facts.

For real products, require usable references. Record recognizable outline, proportions, components, colors, materials, marks and package text. Unseen backs, interiors and dimensions remain unknown. If a user-specified view lacks structural evidence, explain the gap and propose another reference or an achievable alternative view; disclose changes in an alternative deliverable. Without a specified view, a known face may be selected.

Product brands and labels are not watermarks. Consider preparation only when background, occlusion or unrelated annotations obstruct the intended use. Preserve product structure, print and surface condition. Include additional editing in the batch budget; a preliminary white-background edit is not mandatory.

## 2. Give each image a different job

| Purpose | Problem to solve | Practical choices |
|---|---|---|
| Studio / hero | Recognize full form and key features | Choose a revealing angle, broad soft light to control reflections, contact shadows for placement and separation from the background. Background color, reflection and centering depend on the task. |
| Usage scene | Understand how the product is used | Define relationships with surface, setting, people or props. Supporting elements explain use, operation or scale. Check whether each competes with the product; there is no universal prop limit. |
| Detail | Show one real, important feature | Use reference-confirmed structure or material. Side or grazing light can reveal texture; keep the relevant part in focus. A soft background is not a missing detail. |

A coordinated set preserves product characteristics and the agreed visual direction while changing the information each image provides. Renaming backgrounds while keeping the same angle, distance and relationship is insufficient. One requested purpose does not require all three types.

Translate purpose into priorities: a hero retains full outline and recognizable print; a banner reserves a usable text region on the intended side; a detail shows the selected part and adjacent connections; a usage scene shows one plausible relationship among product, people, objects and support surface. Recommend when the user has not chosen; preserve existing choices rather than switching to a habitual setting.

For specific style, materials, space or people, read the relevant section of [photo directions](references/photo-directions.md). For turning a vague brief into a plan, comparing purpose changes or organizing a full prompt, consult the relevant [decisions and worked examples](references/product-photo-examples.md). Simple, clear requests need not load every reference; example products, palettes, people and props are not defaults.

For drinkware opening state, liquids or use actions, read [drinkware structure and state](references/photo-directions.md#drinkware-structure-and-state) as needed.

## 3. Generate and inspect

- Assign reference roles: product images supply visible shape, colors, parts and print; style images help select light and color; layout images supply placement and space; person references establish a requested identity. One input may serve multiple roles if stated. Do not import a style reference's brand, product or person. If the tool exposes a unified `ref` role, explain each input's role in order in the prompt.
- Organize each prompt around "what to retain from the reference → this image's purpose → placement and view → lighting that makes key information readable." Material names need reference or user support. Do not upgrade plastic to metal, invent sealed interiors or add unconfirmed performance claims for appearance. Photographic terms should solve an actual problem, rather than filling paragraphs with parameters. "Exactly like the reference" is not proof of fidelity.
- Check the final prompt against retained and changed features for contradictions. "No added advertising copy" concerns additions while preserving required product print. Follow explicit requests to remove or replace original lettering. Transcribe only source-confirmed text and features; point to the reference and retain uncertainty when unreadable.
- Query current Fish image-generation/editing capabilities and input roles. Choose a path accepting the needed references. Parameters, upload process and pricing follow current tool responses.
- Follow the [shared execution contract](../shared/core-skeleton.md) for execution and records. Include necessary reference preparation and every image attempt in the batch plan.
- Inspect the batch for omissions and product/style drift, then each output against reference structure, colors, components, marks, materials, contact and purpose. Describe defects and impact. Target revisions state changes and retained features.

At delivery, explain each image's purpose and unresolved fidelity issues. Distinguish concepts, prepared references and final product images. Provide execution records under the shared contract.
