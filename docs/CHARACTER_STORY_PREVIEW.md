# Character and narrated-story preview

Two English workflows are available in the GitHub source preview. They have useful task structure and real examples, with known failures retained. Preview means available to try, not certified as consistently better.

## Character sheet

**Purpose:** show one character consistently across requested views, expressions or outfits, and revise selected details while preserving the established identity. Use the result as a design or later-generation reference. A single portrait does not need this workflow.

**Example:** “Create front and back views of one white rabbit, with a blue bow on its own left ear and a purple hoodie.”

**Flow:** reuse the brief/reference → select requested panels → carry identity and anatomical directions through views → generate with supported reference inputs → inspect every panel → revise only the requested difference.

**Evidence:** candidate.3 kept the correct anatomical side in one independent task where the no-Skill Agent changed it. A later clothing edit moved the candidate's rear-view bow to the wrong ear while the control preserved it. Exact preservation and reliable turnaround quality remain unaccepted. It does not guarantee production-ready 3D geometry.

## Narrated multiscene video

**Purpose:** produce one complete story or explainer across multiple scenes, coordinating character references, scene order, starting states/actions, narration and final assembly. Product demonstrations use UGC; transferring source-video actions uses recreation.

**Example:** “Make a 10-second story: a fox takes a book in a library, then opens it on a rooftop under the stars, with these two exact narration lines.”

**Flow:** short scene plan with starting state → ordered action → ending state; bind real references; inspect generated starting images; use actual start-frame conditioning when the state matters; measure exact narration; generate and assemble; inspect the complete film.

A separate paid character sheet is optional. The first usable scene image can supply the identity reference. Independent scenes need no shared identity image. Silence requires no TTS.

**Evidence:** candidate.6 has fresh isolated planning checks, including a new drawer-storage task. Both compared versions planned that new task coherently; extra benefit was not demonstrated. Two actual action clips were generated from candidate.5 plans: the book opens; the umbrella closes and enters the stand after one frame edit and an explicit executor correction from ordinary reference to start-frame input. The fox begins looking upward, so strict “open, then raise head” ordering is not clearly observed. These are targeted clips, not complete candidate.6 narrated-film acceptance.

## Scope of the comparison

- Nine isolated Claude Sonnet 4.6 planning calls in the latest state/conditioning work; all structural checks passed, semantic issues retained.
- Five image calls including one correction, two production Fish video calls, no TTS: 18,750 credits. Reported planning cost: $2.01855.
- Image inspection, contact sheets and end frames are Codex review; full human viewing/listening and repeated stability remain pending.
- Earlier complete-film comparisons remain historical evidence for earlier versions. No same-model HF superiority or undisclosed HF backend mechanism is established.
- The useful HF pattern is task-oriented panels and ordered scene/reference/narration dependencies. These Fish workflows use current Fish tool contracts; they do not import vendor-specific backend interfaces.

[Public examples and comparisons](https://fish-skills-review-20261008.sunny-basil-6485.chatgpt.site/expansion.html) · [Exact source hashes and evidence scope](evidence/character-story-preview-20261009.json)

This update pushes source to GitHub. A versioned Release, R2 channel activation and production Skill availability are separate actions.
