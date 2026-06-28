import os
import subprocess
from datetime import datetime

from app.config import FFMPEG_PATH

VIDEO_OUTPUT_DIR = os.path.join("storage", "video_output")
os.makedirs(VIDEO_OUTPUT_DIR, exist_ok=True)


def merge_audio_with_video(video_path: str, audio_path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_video_path = os.path.join(
        VIDEO_OUTPUT_DIR,
        f"translated_video_{timestamp}.mp4"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-shortest",
        output_video_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_video_path
