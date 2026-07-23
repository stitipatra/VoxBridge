import os
import subprocess
from datetime import datetime
from app.services.tts_service import generate_speech
from app.config import FFMPEG_PATH, FFPROBE_PATH

VIDEO_OUTPUT_DIR = os.path.join("storage", "video_output")
AUDIO_OUTPUT_DIR = os.path.join("storage", "audio_output")
FONTS_DIR = os.path.join("tools", "fonts")

os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)


def _format_path_for_ffmpeg(path: str) -> str:
    absolute_path = os.path.abspath(path)
    formatted_path = absolute_path.replace("\\", "/")
    formatted_path = formatted_path.replace(":", "\\:")
    return formatted_path


def get_media_duration(path: str) -> float:
    command = [
        FFPROBE_PATH,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return float(result.stdout.strip())


def get_video_dimensions(video_path: str) -> tuple[int, int]:
    command = [
        FFPROBE_PATH,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        video_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    width, height = result.stdout.strip().split(",")
    return int(width), int(height)


def build_atempo_filter(speed_factor: float) -> str:
    factors = []

    while speed_factor < 0.5:
        factors.append(0.5)
        speed_factor /= 0.5

    while speed_factor > 2.0:
        factors.append(2.0)
        speed_factor /= 2.0

    factors.append(speed_factor)

    return ",".join(f"atempo={factor:.4f}" for factor in factors)


def match_audio_duration(
    audio_path: str,
    target_duration: float
) -> str:
    audio_duration = get_media_duration(audio_path)

    if audio_duration <= 0:
        raise ValueError(
            f"Invalid generated audio duration: {audio_duration}"
        )

    if target_duration <= 0:
        raise ValueError(
            f"Invalid target duration: {target_duration}"
        )

    speed_factor = audio_duration / target_duration
    filters = []

    # Generated speech is longer than the available duration.
    # Speed it up enough to fit.
    if speed_factor > 1.03:
        filters.append(
            build_atempo_filter(speed_factor)
        )

    # Generated speech is shorter than the available duration.
    # Slow it down, but by no more than 30%.
    elif speed_factor < 0.97:
        safe_speed_factor = max(
            speed_factor,
            1 / 1.30
        )

        filters.append(
            build_atempo_filter(safe_speed_factor)
        )

    # Fill any remaining gap with silence and force
    # the output to exactly match target_duration.
    filters.extend([
        f"apad=pad_dur={target_duration:.4f}",
        f"atrim=0:{target_duration:.4f}",
        "asetpts=N/SR/TB"
    ])

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    adjusted_audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"duration_matched_audio_{timestamp}.wav"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", audio_path,
        "-filter:a", ",".join(filters),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        adjusted_audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Audio duration matching failed:\n"
            f"{result.stderr}"
        )

    return adjusted_audio_path


def generate_segment_audio_clips(
    translated_segments: list[dict],
    target_language: str,
    voice_gender: str
) -> list[dict]:
    """
    Generate one temporary TTS clip for every translated segment
    and match it to the segment's exact duration.

    Returns:
        [
            {
                "start": 0.0,
                "end": 2.5,
                "duration": 2.5,
                "text": "Translated sentence",
                "audio_path": "...wav",
                "temporary_paths": [
                    "...original_tts.wav",
                    "...duration_matched.wav"
                ]
            }
        ]
    """

    segment_audio_clips = []

    try:
        for index, segment in enumerate(translated_segments):
            start_time = float(segment.get("start", 0.0))
            end_time = float(segment.get("end", 0.0))
            translated_text = str(
                segment.get("text", "")
            ).strip()

            segment_duration = end_time - start_time

            if not translated_text:
                continue

            if segment_duration <= 0:
                raise ValueError(
                    f"Invalid duration for translated segment "
                    f"{index}: start={start_time}, end={end_time}"
                )

            # Generate the raw TTS audio for this segment.
            raw_audio_path = generate_speech(
                translated_text,
                target_language,
                voice_gender
            )

            if not raw_audio_path or not os.path.exists(
                raw_audio_path
            ):
                raise RuntimeError(
                    f"TTS generation failed for segment {index}"
                )

            # Force the generated speech to fit exactly inside
            # the original Whisper segment duration.
            matched_audio_path = match_audio_duration(
                raw_audio_path,
                segment_duration
            )

            if not os.path.exists(matched_audio_path):
                raise RuntimeError(
                    f"Duration matching failed for segment {index}"
                )

            segment_audio_clips.append({
                "start": start_time,
                "end": end_time,
                "duration": segment_duration,
                "text": translated_text,
                "audio_path": matched_audio_path,
                "temporary_paths": [
                    raw_audio_path,
                    matched_audio_path
                ]
            })

        if not segment_audio_clips:
            raise ValueError(
                "No valid translated segments were available "
                "for synchronized audio generation."
            )

        return segment_audio_clips

    except Exception:
        # Clean up anything generated before the failure.
        for clip in segment_audio_clips:
            for temporary_path in clip.get(
                "temporary_paths",
                []
            ):
                try:
                    if (
                        temporary_path
                        and os.path.exists(temporary_path)
                    ):
                        os.remove(temporary_path)
                except OSError:
                    pass

        raise


def create_synchronized_audio(
    segment_audio_clips: list[dict]
) -> tuple[str, list[str]]:
    """
    Create one synchronized narration audio by placing every
    segment audio at its original Whisper timestamp.

    Returns:
        (
            synchronized_audio_path,
            temporary_files_created
        )
    """

    if not segment_audio_clips:
        raise ValueError(
            "No segment audio clips provided."
        )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    synchronized_audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"synchronized_audio_{timestamp}.wav"
    )

    filter_parts = []
    input_args = []
    temporary_files = []

    for index, clip in enumerate(segment_audio_clips):
        audio_path = clip["audio_path"]
        start_time = float(clip["start"])

        delay_ms = int(start_time * 1000)

        input_args.extend([
            "-i",
            audio_path
        ])

        filter_parts.append(
            f"[{index}:a]"
            f"adelay={delay_ms}|{delay_ms}"
            f"[a{index}]"
        )

        temporary_files.append(audio_path)

    mix_inputs = "".join(
        f"[a{i}]"
        for i in range(len(segment_audio_clips))
    )

    filter_parts.append(
        f"{mix_inputs}"
        f"amix=inputs={len(segment_audio_clips)}:"
        f"normalize=0"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        *input_args,
        "-filter_complex",
        ";".join(filter_parts),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        synchronized_audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Failed to create synchronized audio:\n"
            f"{result.stderr}"
        )

    return synchronized_audio_path


def merge_audio_with_video(
    video_path: str,
    audio_path: str,
    subtitle_path: str | None = None
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    output_video_path = os.path.join(
        VIDEO_OUTPUT_DIR,
        f"translated_video_{timestamp}.mp4"
    )

    video_duration = get_media_duration(video_path)
    audio_path = match_audio_duration(audio_path, video_duration)

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
    ]

    if subtitle_path:
        formatted_subtitle_path = _format_path_for_ffmpeg(subtitle_path)
        formatted_fonts_dir = _format_path_for_ffmpeg(FONTS_DIR)

        subtitle_filter = (
            f"ass='{formatted_subtitle_path}'"
            f":fontsdir='{formatted_fonts_dir}'"
        )

        command.extend([
            "-vf",
            subtitle_filter,
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "23",
        ])
    else:
        command.extend([
            "-c:v",
            "copy",
        ])

    command.extend([
        "-c:a",
        "aac",
        output_video_path
    ])

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_video_path
