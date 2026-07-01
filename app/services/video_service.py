import os
import subprocess
from datetime import datetime

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


def match_audio_duration(audio_path: str, target_duration: float) -> str:
    audio_duration = get_media_duration(audio_path)

    if audio_duration <= 0 or target_duration <= 0:
        return audio_path

    speed_factor = audio_duration / target_duration

    if 0.97 <= speed_factor <= 1.03:
        return audio_path

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    adjusted_audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"duration_matched_audio_{timestamp}.wav"
    )

    atempo_filter = build_atempo_filter(speed_factor)

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", audio_path,
        "-filter:a", atempo_filter,
        adjusted_audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return adjusted_audio_path


def merge_audio_with_video(
    video_path: str,
    audio_path: str,
    subtitle_path: str | None = None
) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

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
