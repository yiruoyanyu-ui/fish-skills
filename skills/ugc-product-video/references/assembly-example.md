# Executable Audio/Video Assembly Example

Read only after choosing separate narration tracks and needing local assembly. If the original track satisfies the copy, voice and action-alignment requirements, use the inspected original directly. Use the [assembly helper](../scripts/assemble_voiceover.py); this path requires local `python3`, `ffmpeg` and `ffprobe`. Disclose unperformed assembly or use an available editor when tools are missing. Local assembly does not call a generation service.

## Establish the actual timeline

Protect original footage and narration; output to a new path. Set narration starts from actual actions and cuts. The helper confirms the first video track's duration and the first audio track's duration in each narration file. `keep/lower` also confirm the source audio track they use. Stop when a required duration is unknown; container duration is not footage length. `replace` does not use source audio and does not require its duration or start offset.

Edit multiple shots into one timeline before narration. If codec, ratio, frame rate and audio layout match, create `shots.txt` in the working directory:

```text
file 'shot-01.mp4'
file 'shot-02.mp4'
```

```bash
ffmpeg -nostdin -n -f concat -safe 1 -i shots.txt -c copy timeline.mp4
ffprobe -v error -show_entries stream=index,codec_type,start_time,duration -of json timeline.mp4
```

Create a same-directory list from verified materials for this task. Normalize incompatible clips with an editor. Watch the concatenation and use observed cuts/actions, not estimated prompt timings.

## Choose source-audio handling for this task

- `replace`: Use only new narration. Replace duplicate or inseparable original speech to avoid simultaneous speakers. Obtain separate tracks or an editing plan when on-site audio must remain.
- `keep`: Retain source sound and mix narration when conflict-free ambience is confirmed. Listen for balance and overlap.
- `lower`: Multiply the entire original track by a chosen gain, e.g. `--source-volume 0.15`. Fixed reduction does not remove speech or provide automatic ducking.

`keep/lower` support only a confirmed zero relative start offset between source audio and video. Apart from a one-microsecond numerical tolerance in metadata, a nonzero offset or an unknown start time on either track is rejected. First normalize the timeline in an editor while preserving audio/video synchronization. The helper does not automatically move source audio to repair the input. With no original audio, `keep/lower` use only new narration and the report states that fact.

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

Only when a frozen tail is permitted and still meets duration requirements, add `--allow-tail-freeze --tail-pad 0.2`. This extends the last frame through narration and a pause whose length follows the pacing; it does not repair action/narration mismatch. For strict duration, adjust footage and copy first.

The report includes durations of the source tracks used and final tracks, last narration end, planned duration, tail extension, source-audio presence and the relative start offset checked for `keep/lower`. `replace` does not check the offset and reports that field as `null`. A 2-second picture with 4-second source audio still needs picture extension for 3-second narration; container duration does not satisfy it. A complete render is published atomically and exclusively from the output directory, never overwriting an existing file. Peak limiting does not guarantee appropriate background/voice balance or delivery.

## Subtitles and delivery

Follow the user's subtitle choice; add none when requested. When needed, make SRT from final copy and measured starts, confirm the text, then choose sidecar or burned-in subtitles. Deliver sidecar SRT with the video; it is not visible in the image. Burn to a new file and inspect legibility, occlusion and synchronization. The helper does not add subtitles by default.

Use available capabilities to watch and listen to the entire result. Check narration/action alignment, duplicate speech, complete endings, subtitles and duration; record unchecked items. Preserve original footage, segment times, assembly settings and the final version. Separate files are not a substitute for a requested complete video.
