# Ordered scene assembly

Use a manifest whose entries contain `index`, source clip, intended scene duration, exact narration text, narration file, actual measured durations, and any subtitle/alignment source. Keep output path and expected total duration explicit. Paths are actual available files, not future promises.

Before rendering, probe every input; reject a missing clip or audio, wrong ordering, impossible timing or unsupported required format. Derive frame rate and dimensions from the actual clip(s), normalize only when needed and record it. Preserve source clips and assemble to a new file.

Place each narration take within its assigned scene without clipping speech. If it exceeds the window, revise/regenerate or adjust the allocation within the brief rather than silently stretch it. Mixed native audio needs an explicit decision; do not accidentally retain native dialogue under the narrator.

After rendering, probe total duration, geometry and audio/video streams, then inspect the complete film. Deterministic metadata cannot verify semantic scene continuity or pronunciation. Mark those checks separately.

For a simple no-subtitle two-scene film, ordinary FFmpeg processing is sufficient if available. A fixed executable helper should be added only after the common manifest and actual cases establish its reusable needs; this guide does not assume HF's installed scripts exist in Fish.
