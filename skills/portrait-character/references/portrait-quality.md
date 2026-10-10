# Portrait Review and Targeted Revision

Use this guide only when the current host can inspect image pixels, the user requests a visual critique, or a visual-capable reviewer has supplied concrete observations. It is not a required post-generation stage. A text-only Agent delivers the result without inventing visual findings.

Review a generated portrait, a reference-based edit or an existing user image against its intended use and source material. Describe specific visible evidence rather than concluding only that it feels "AI-generated," "unnatural" or "more premium."

## Two-pass review

First inspect the image at its intended display size. Check whether the person is recognizable, expression and pose communicate the intended state, and styling, setting, composition and medium form one coherent result.

Then inspect only relevant regions at the available native resolution: face and hairline, eyes and mouth, hands, neck and shoulders, wardrobe edges, accessories, and contact between the person and objects. Do not treat enlarged interpolation as source detail.

| Area | Observable questions |
|---|---|
| Brief and medium | Are person count, age range, styling, medium, framing and explicit requirements present? Is intentional retouching or stylization preserved? |
| Identity and continuity | With a reference, did facial relationships, hair, build or signature details drift unexpectedly? Across a series, is the person still recognizable as the same character? |
| Expression and gaze | Do the eyes, mouth, head direction and body posture communicate the same state and fit the person's relationship to the scene? |
| Structure and contact | Are facial features, ears, teeth, fingers, shoulders, neck and limbs coherent? Do hair, collars, accessories or held objects merge, intersect or make incorrect contact? |
| Materials and light | In realistic work, is skin unintentionally waxy or over-smoothed? Do hair and fabric retain suitable structure? Are the face, body, wardrobe and environment lit coherently? |
| Composition and use | Do scale, crop, space and clarity suit the intended output? Judge avatars, half-body portraits and full-body images by their different purposes. |

## Targeted revision

A revision instruction should state:

1. The observed issue and its location.
2. The attribute to change in this attempt.
3. The identity, styling, pose, setting or medium that must remain.
4. The region that a visual-capable reviewer should recheck afterward.

Prioritize defects that prevent the requested use or recognition. A local defect does not automatically require recreating the whole image. If an editing path may introduce larger identity drift, explain the tradeoff before proceeding.

When the current Agent cannot inspect the revised result, it must not claim that the defect was fixed; deliver the revision and request confirmation. When inspection is available, check the whole image for newly introduced drift rather than checking only the edited region.

Naturalness is not determined by any single skin texture, grain setting, camera parameter or degree of symmetry. Likeness to a specific real person requires side-by-side comparison with the source and final confirmation from the user. Leave details unknown when the evidence is insufficient.
