---
name: portrait-character
description: Create or edit person-led still images such as fictional character portraits, avatars, editorial portraits and reference-based portrait changes. Use when identity, expression, styling, pose or continuity across images matters. A specific real person or established character requires a usable identity reference; without one, create a new character rather than promising likeness.
---

# Portrait and Character Image · v0.1-candidate.3

Experimental preview. Build the image around the person the user wants to portray, coordinating identity, styling, expression, pose, composition and visual treatment. References can improve continuity, but they do not guarantee identity or detail fidelity.

## 1. Establish the person and deliverable

Reuse the brief to determine the image's purpose, number of people, framing, aspect ratio, style and requested changes. Ask only when a missing choice would materially change identity or delivery. If the user delegates creative choices, state the chosen direction briefly and continue.

Distinguish the identity basis:

- **New fictional character:** design a new person from the written brief. Additional appearance, wardrobe and photographic choices are creative decisions, not user-provided facts.
- **Established character:** use the supplied or user-selected character image as the appearance source. Separate traits that must remain stable from traits that may change. Unseen or unclear details remain unknown unless the user accepts a proposed design.
- **Specific real person:** require a usable source image for likeness. State the intended change and the areas that should remain unchanged. Do not substitute a text-generated lookalike for the person.

Preserve explicit choices about age, body type, skin tone, makeup, retouching and medium. Convey profession, temperament or story role through expression, pose, wardrobe and context rather than assigning a stereotyped face or body.

## 2. Develop the character direction

For a vague brief, a new character design or cross-image continuity, read [portrait directions](references/portrait-recipes.md). A clear, simple request does not need every dimension in that guide.

Separate stable identity from the state of this image:

- Stable identity may include recognizable facial relationships, hair shape or color, body build, signature styling and continuity details.
- Current state may include expression, gaze, action, wardrobe changes, setting, composition and lighting.

Use a small number of coordinated, recognizable traits instead of stacking adjectives. Expression, gaze and pose should describe the same moment. Photographic or illustrative choices serve the requested use; do not impose a universal lens, lighting setup, grain level or skin treatment.

Organize the generation or editing instruction with only the information the task needs:

```text
identity and stable traits → current expression, gaze and action → styling
→ setting and composition → lighting or visual medium → retain/change constraints
```

Explain what each reference contributes, such as identity, styling, pose, layout or visual treatment. Do not import the person from a style reference unless that person is also the intended identity.

## 3. Generate or edit

Select a current image-generation or editing path that supports the required references. Prefer a reference-capable editing path for a specific person, an established character or a localized change. If the available tool cannot use a reference in the required role, explain the limitation and offer an achievable alternative; do not invent face locking, identity training or local-control capabilities.

For an edit, state the requested change first, followed by only the relevant identity, age, skin tone, build, hair, wardrobe, background or composition traits that must remain. A trait the user wants changed cannot also appear in the retention list.

For a recurring character, reuse the user-selected result as the next appearance reference and keep a short character record when continuity is actually needed. A reference input improves continuity but does not guarantee it; it does not require every character to have a turnaround sheet or trained identity model.

Follow the [shared execution contract](../shared/core-skeleton.md) for capability discovery, estimates, authorization, job recovery and delivery records.

## 4. Deliver and optionally review

After generation, confirm the job status and deliver the returned image or file together with the actual generation description. Successful delivery does not mean the pixels were visually inspected.

Read [portrait review and targeted revision](references/portrait-quality.md) only when the current host can inspect the image, the user asks for a critique, or a visual-capable reviewer supplies concrete feedback. If visual inspection is unavailable, say so without guessing about likeness, anatomy, materials, lighting or image quality.

Run a targeted revision only after a specific defect has been identified and another attempt is authorized. Name the affected region, the observable change and the traits that must remain. Do not automatically repeat generation until the result seems satisfactory.

Deliver unresolved issues that were actually observed. The user makes the final judgment about whether a specific real person's likeness is acceptable.
