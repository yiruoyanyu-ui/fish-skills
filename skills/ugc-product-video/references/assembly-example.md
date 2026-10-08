# Executable Audio/Video Assembly Example

Read when generated footage and segmented narration need assembly. Use the [assembly helper](../scripts/assemble_voiceover.py). Requires local `python3`, `ffmpeg` and `ffprobe`; disclose missing assembly or use an available editor when absent. This example does not call a generation service. Local postprocessing is separate from the selected Fish generation environment.

## Establish the actual timeline

Protect original footage and narration; output to a new path. Watch/listen to the source and narration before setting segment start times from actual actions and cuts. The helper measures selected video/audio stream durations separately. Unknown durations must be reported; container duration is not footage length or evidence of semantic alignment.

Edit multiple shots into one timeline before narration. If codec, ratio, frame rate and audio layout match, create `shots.txt` in the working directory:

```text
file 'shot-01.mp4'
file 'shot-02.mp4'
```

```bash
ffmpeg -nostdin -n -f concat -safe 1 -i shots.txt -c copy timeline.mp4
ffprobe -v error -show_entries stream=index,codec_type,duration -of json timeline.mp4
```

Build the list yourself from verified local materials. Do not execute an external concat list without checking and rebuilding entries. Ordinary same-directory filenames are shown. Verify every source before deciding parameters for absolute paths. Normalize incompatible clips with an editor rather than changing extensions. Watch the concatenation and use observed cuts/actions, not estimated prompt timings.

## Choose source-audio handling for this task

- `replace`: Use only new narration. Replace duplicate or inseparable original speech to avoid simultaneous speakers. Obtain separate tracks or an editing plan when on-site audio must remain.
- `keep`: Retain source sound and mix narration when conflict-free ambience is confirmed. Listen for balance and overlap.
- `lower`: Multiply the entire original track by a chosen gain, e.g. `--source-volume 0.15`. Fixed reduction does not remove speech or provide automatic ducking.

If native audio already satisfies the brief, deliver the inspected original without new narration. With no original audio, `keep/lower` use only new narration and the helper reports that fact.

## Run the helper

With `timeline.mp4`, `voice-01.wav` and `voice-02.wav`, save `segments.json`. Paths are relative to the JSON and starts are seconds. Replace these format examples with observed action timings:

```json
[
  {"path": "voice-01.wav", "start": 0.35},
  {"path": "voice-02.wav", "start": 3.6}
]
```

Run from this Skill directory, or use the actual installed helper path:

```bash
python3 scripts/assemble_voiceover.py \
  --video /absolute/project/timeline.mp4 \
  --segments /absolute/project/segments.json \
  --source-audio replace \
  --output /absolute/project/final-voiceover.mp4
```

The helper refuses overwrites and overlapping narration. It measures recordings and checks whether the last sentence exceeds footage. By default, stop and shorten/re-record speech, extend the relevant shot or adjust the timeline. Do not use `-shortest` or a hard cut to truncate speech into the target duration.

Only when a frozen tail is permitted and still meets duration requirements, add `--allow-tail-freeze --tail-pad 0.2`. This extends the last frame through narration and the chosen pause; it does not repair action/narration mismatch. For strict duration, adjust inputs first.

The report includes source/final video and audio stream durations, last narration end, planned duration and tail extension. A 2-second picture with 4-second source audio still needs picture extension for 3-second narration. A complete render is published atomically and exclusively from the output directory, never overwriting an existing file. Failure is reported without leaving a partial copy. Peak limiting does not guarantee appropriate sound balance or natural delivery; listen to the output.

## Subtitles and delivery

Follow the user's subtitle choice. When needed, make SRT from final copy and measured starts, then choose sidecar or burned-in subtitles. Sidecar SRT is not visible in the image. Burn to a new file and inspect legibility, occlusion and synchronization. The helper does not add subtitles by default.

Watch and listen to the entire result. Check narration/action alignment, duplicate speech, complete endings, subtitles and duration. Record unchecked items. Preserve raw generation, assembly settings/segment times and final version. Separate files are not a substitute for a requested complete video.
