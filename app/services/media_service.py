import os
import subprocess
from datetime import datetime

from app.config import FFMPEG_PATH, AUDIO_OUTPUT_DIR


def extract_audio_from_video(video_path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"extracted_audio_{timestamp}.wav"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_audio_path


def convert_audio_to_wav(audio_path: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_audio_path = os.path.join(
        AUDIO_OUTPUT_DIR,
        f"converted_audio_{timestamp}.wav"
    )

    command = [
        FFMPEG_PATH,
        "-y",
        "-i", audio_path,
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        output_audio_path
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_audio_path
