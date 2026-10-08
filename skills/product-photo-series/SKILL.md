---
name: product-photo-series
description: |
  Create studio, usage-scene, detail or coordinated commercial product images from product references, or edit existing product photos.
  Use for product photography, ecommerce hero images, contextual shots and detail close-ups. Planning or critique alone does not trigger generation.
  Real-product fidelity requires reference photos; text-only briefs must explicitly accept concept images rather than exact reconstruction.
---

# Commercial Product Photography · v0.4-candidate.5

Status: experimental research draft. This revision reorganizes shared execution dependencies. Candidate.4 results and its rejection are historical evidence, not acceptance of this version. The English adaptation has not undergone a new behavior or media comparison.

Use references as the source of product appearance. Vary scene, viewpoint, lighting and distance to serve different image purposes. References help fidelity but outputs still require inspection. Historical evidence mainly concerns drinkware; fidelity and usability for other categories need separate validation.

## 1. Define the deliverable and materials

Use the existing brief to establish where the image will appear, what it should communicate, image count and aspect ratio. A single-image request stays a single image; square output is not mandatory.

Treat these choices independently. Studio photography does not imply no people, and a usage scene does not imply a handheld product.

| Choice | Decision basis |
|---|---|
| Use | Hero images prioritize recognition; details explain; ads attract attention and accommodate information. Adopt the user's platform and layout requirements. |
| Image type | Studio shots show form; contextual shots show environment or use; details explain a component. These are options, not a required three-image package. |
| People | No person, hands, partial person or model, depending on scale, operation, wearing or brand expression. Keep the product recognizable. |
| Visual direction | Choose clean, dramatic, warm, vivid or another direction for the product and purpose. "Premium" does not automatically mean dark, minimal or unoccupied. |

### When to ask and when to decide

- Reuse stated purpose, people, ratio and style without asking again. The Agent handles exposure, light placement and depth of field; the user need not know photographic terminology.
- For "make a product image series," ask only the choices that materially change the deliverable, with a short recommendation. For example: "I suggest a hero, usage scene and detail. Would you prefer an unoccupied environment or a handheld demonstration?" This is an example, not a mandatory interview template.
- If the user is unsure, explain the practical difference and recommend a direction. An unoccupied setting emphasizes product and space; hands can clarify scale or operation. Let the user choose or delegate.
- If the user says "you decide," "just make it" or "don't ask," proceed with a brief statement of the plan. Without purpose clues, begin with clear overall appearance. Give each image a purpose rather than inventing a person, window or drinking action.
- Unspecified settings are creative choices, not user requirements or proven product functions. Recommendations remain overridable; materials and spending still follow the actual task and authorization.

For real products, require usable references. Record recognizable outline, proportions, components, colors, visible surface appearance, marks and readable package text. Unseen backs, interiors and dimensions remain unknown. If a requested view needs missing information, choose a known view or request another photo rather than inventing real structure.

Product brands and labels are not watermarks. Consider preparation only when background, occlusion or unrelated annotations obstruct the intended use. Preserve product structure, print and surface condition. Include additional editing in the batch budget; a preliminary white-background edit is not mandatory.

## 2. Give each image a different job

| Purpose | Problem to solve | Practical choices |
|---|---|---|
| Studio / hero | Recognize full form and key features | Choose a revealing angle, broad soft light to control reflections, contact shadows for placement and separation from the background. Background color, reflection and centering depend on the task. |
| Usage scene | Understand how the product is used | Define relationships with surface, setting, people or props. Supporting elements explain use, operation or scale. Check whether each competes with the product; there is no universal prop limit. |
| Detail | Show one real, important feature | Use reference-confirmed structure or material. Side or grazing light can reveal texture; keep the relevant part in focus. A soft background is not a missing detail. |

A coordinated set preserves product characteristics and the agreed visual direction while changing the information each image provides. Renaming backgrounds while keeping the same angle, distance and relationship is insufficient. One requested purpose does not require all three types.

Translate purpose into priorities: a hero retains full outline and recognizable print; a banner reserves a usable text region on the intended side; a detail shows the selected part and adjacent connections; a usage scene shows one plausible relationship among product, people, objects and support surface. Recommend when the user has not chosen; preserve existing choices.

For specific style, materials, space or people, read the relevant section of [photo directions](references/photo-directions.md). For turning a vague brief into a plan, changing purpose or organizing a full prompt, consult [decisions and worked examples](references/product-photo-examples.md). Simple requests need not load every reference; example products, palettes, people and props are not defaults.

Read [drinkware guidance](references/category-thermos.md) only for drinkware opening, steam or usage actions. Other categories do not inherit it.

## 3. Generate and inspect

- Assign reference roles: product images supply visible shape, colors, parts and print; style images supply light and color direction; layout images supply placement and space; person references establish a requested identity. One input may serve multiple roles if stated. Do not import a style reference's brand, product or person. If the tool exposes a unified `ref` role, explain each input's role in order in the prompt.
- Organize each prompt around "what to retain from the reference → this image's purpose → placement and view → lighting that makes key information readable." Material names need reference or user support. Do not upgrade plastic to metal, invent sealed interiors or add unconfirmed performance claims for sophistication. Photographic terms should solve an actual problem. "Exactly like the reference" is not proof of fidelity.
- Text, branding, people, props and atmosphere follow this brief. Unsupported functions or performance are not selling points. Briefly reflect user overrides in the plan.
- Check the final prompt against retained and changed features for contradictions. "No added advertising copy" concerns additions while preserving required product print. Follow explicit requests to remove or replace original lettering. Transcribe only source-confirmed text and features; point to the reference and retain uncertainty when unreadable.
- Query current Fish image-generation/editing capabilities and input roles. Choose a path accepting the needed references. Parameters, upload process and pricing follow current tool responses.
- Follow the [shared execution contract](../shared/core-skeleton.md) for spending, idempotent submission, original-job queries, inspection disclosure and delivery status. Visual choices and material requirements follow this Skill and the brief.
- Budget the complete batch, including preparation and attempt limits. Use applicable existing authorization. Preserve actual prompts, calls, all outputs and costs.
- Inspect the batch for omissions and product/style drift, then each output against reference structure, colors, components, marks, visible material appearance, contact and purpose. Describe defects and impact. Target revisions state changes and retained features and consume the attempt allowance. One unsuccessful revision does not prove a model ceiling or justify a ban for unrelated products. Disclose when visual inspection was not performed.

Deliver images, their purposes, actual prompts, model/parameters, costs and unresolved fidelity issues. Distinguish concepts, prepared references and final product images. Job success is not quality acceptance.
