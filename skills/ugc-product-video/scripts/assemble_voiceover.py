#!/usr/bin/env python3
"""Mix timed narration into a video without overwriting sources or cutting speech."""

import argparse
import json
import math
import os
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import tempfile


def probe(path, duration_kinds=("video", "audio")):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)],
        check=True, capture_output=True, text=True,
    )
    info = json.loads(result.stdout)
    durations = {}
    streams = {}
    # Match the first video/audio streams selected by the assembly command.
    # Container duration may follow a longer unrelated track; it is not footage length.
    for stream in info["streams"]:
        kind = stream["codec_type"]
        if kind not in ("video", "audio") or kind in streams:
            continue
        streams[kind] = stream
        if kind not in duration_kinds:
            continue
        try:
            duration = float(stream["duration"])
        except (KeyError, TypeError, ValueError):
            try:
                duration = float(stream["duration_ts"] * Fraction(stream["time_base"]))
            except (KeyError, TypeError, ValueError, ZeroDivisionError):
                raise ValueError(f"Cannot confirm {kind} track duration: {path}") from None
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError(f"Cannot confirm a positive {kind} track duration: {path}")
        durations[kind] = duration
    return durations, streams


def source_audio_offset(streams, path):
    starts = {}
    for kind in ("video", "audio"):
        stream = streams[kind]
        try:
            start = float(stream["start_time"])
        except (KeyError, TypeError, ValueError):
            try:
                start = float(stream["start_pts"] * Fraction(stream["time_base"]))
            except (KeyError, TypeError, ValueError, ZeroDivisionError):
                raise ValueError(
                    f"Cannot confirm source {kind} start time: {path}. "
                    "For keep/lower, first normalize the timeline in an editor "
                    "while preserving audio/video synchronization."
                ) from None
        if not math.isfinite(start):
            raise ValueError(
                f"Cannot confirm source {kind} start time: {path}. "
                "For keep/lower, first normalize the timeline in an editor "
                "while preserving audio/video synchronization."
            )
        starts[kind] = start
    offset = starts["audio"] - starts["video"]
    # This helper resets both streams. Reject a measurable relative start offset
    # instead of silently moving existing audio relative to the picture.
    if abs(offset) > 0.000001:
        raise ValueError(
            f"Source audio starts {offset:+.6f}s relative to video: {path}. "
            "For keep/lower, first normalize the timeline in an editor "
            "while preserving audio/video synchronization."
        )
    return offset


def number(value, name):
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a nonnegative number")
    value = float(value)
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a nonnegative number")
    return value


def assemble(args):
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise ValueError(f"Required local tool is unavailable: {tool}")
    source = args.video.resolve(strict=True)
    manifest = args.segments.resolve(strict=True)
    output = args.output.resolve()
    if output.suffix.lower() != ".mp4":
        raise ValueError("Output must be an .mp4 file")
    if output.exists():
        raise ValueError(f"Output already exists; choose a new path: {output}")
    used_source_kinds = ("video",) if args.source_audio == "replace" else ("video", "audio")
    source_tracks, source_streams = probe(source, used_source_kinds)
    if "video" not in source_tracks:
        raise ValueError("Source has no video stream")
    source_duration = source_tracks["video"]
    original_offset = None
    if args.source_audio != "replace" and "audio" in source_streams:
        original_offset = source_audio_offset(source_streams, source)
    rows = json.loads(manifest.read_text())
    if not isinstance(rows, list) or not rows:
        raise ValueError("Segments must be a nonempty JSON array")
    segments = []
    for row in rows:
        path = (manifest.parent / row["path"]).resolve(strict=True)
        tracks, _ = probe(path, ("audio",))
        if "audio" not in tracks:
            raise ValueError(f"Narration has no audio stream: {path}")
        duration = tracks["audio"]
        # adelay uses whole milliseconds; use the same value for end-time checks.
        start_ms = round(number(row["start"], "start") * 1000)
        segments.append((start_ms, duration, path))
    segments.sort(key=lambda item: item[0])
    previous_end = 0.0
    for start_ms, duration, path in segments:
        if start_ms / 1000 < previous_end - 0.001:
            raise ValueError(f"Narration segments overlap: {path}; revise the timeline")
        previous_end = start_ms / 1000 + duration
    tail_pad = number(args.tail_pad, "tail-pad")
    source_volume = number(args.source_volume, "source-volume")
    target_duration = max(source_duration, previous_end + tail_pad)
    extension = target_duration - source_duration
    if extension > 0.001 and not args.allow_tail_freeze:
        raise ValueError(
            f"Narration/tail needs {target_duration:.3f}s; source is {source_duration:.3f}s. "
            "Revise speech or footage, or explicitly allow a frozen last frame with --allow-tail-freeze."
        )
    filters = []
    video_filter = "setpts=PTS-STARTPTS"
    if extension > 0:
        video_filter += f",tpad=stop_mode=clone:stop_duration={extension:.6f}"
    filters.append(f"[0:v:0]{video_filter},trim=duration={target_duration:.6f}[v]")
    audio_labels = []
    if args.source_audio != "replace" and "audio" in source_tracks:
        volume = source_volume if args.source_audio == "lower" else 1.0
        filters.append(
            f"[0:a:0]asetpts=PTS-STARTPTS,aresample=48000,"
            f"aformat=channel_layouts=stereo,volume={volume},"
            f"apad,atrim=duration={target_duration:.6f}[original]"
        )
        audio_labels.append("[original]")
    for index, (start_ms, duration, path) in enumerate(segments, start=1):
        filters.append(
            f"[{index}:a:0]asetpts=PTS-STARTPTS,aresample=48000,"
            f"aformat=channel_layouts=stereo,adelay={start_ms}:all=1[voice{index}]"
        )
        audio_labels.append(f"[voice{index}]")
    filters.append(
        "".join(audio_labels)
        + f"amix=inputs={len(audio_labels)}:duration=longest:normalize=0,"
        + f"alimiter=limit=0.95:level=0:latency=1,apad,atrim=duration={target_duration:.6f}[a]"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    # Render on the same filesystem; publish the complete file with an exclusive link.
    with tempfile.TemporaryDirectory(prefix="ugc-assembly-", dir=output.parent) as temp:
        rendered = Path(temp) / "rendered.mp4"
        command = ["ffmpeg", "-nostdin", "-v", "error", "-n", "-i", str(source)]
        for start_ms, duration, path in segments:
            command += ["-i", str(path)]
        command += [
            "-filter_complex", ";".join(filters), "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
            "-b:a", "192k", "-movflags", "+faststart", str(rendered),
        ]
        subprocess.run(command, check=True)
        actual_tracks, _ = probe(rendered)
        if not {"video", "audio"}.issubset(actual_tracks):
            raise ValueError("Rendered file is missing video or audio")
        actual_duration = actual_tracks["video"]
        # Check both selected tracks; a longer container/audio duration cannot pass video.
        for kind, duration in actual_tracks.items():
            if duration + 0.05 < target_duration:
                raise ValueError(f"Rendered {kind} track is too short: {duration:.3f}s")
        try:
            os.link(rendered, output)
        except FileExistsError:
            raise ValueError(f"Output already exists; choose a new path: {output}") from None
    print(json.dumps({
        "output": str(output), "source_duration": source_duration,
        "narration_end": previous_end, "planned_duration": target_duration,
        "actual_duration": actual_duration, "tail_freeze": extension,
        "source_track_durations": source_tracks,
        "actual_track_durations": actual_tracks,
        "source_audio": args.source_audio,
        "source_audio_present": "audio" in source_streams,
        "source_audio_relative_start": original_offset,
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--video", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True,
                        help="JSON array: [{\"path\": \"voice.wav\", \"start\": 0.4}]")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-audio", choices=("replace", "keep", "lower"), required=True)
    parser.add_argument("--source-volume", type=float, default=0.2,
                        help="Fixed original-track volume for lower mode; not automatic ducking")
    parser.add_argument("--tail-pad", type=float, default=0,
                        help="Seconds after the final narration segment")
    parser.add_argument("--allow-tail-freeze", action="store_true",
                        help="Explicitly allow extending video with its last frame")
    try:
        assemble(parser.parse_args())
    except (ValueError, KeyError, TypeError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Assembly failed: {error}\n")


if __name__ == "__main__":
    main()
