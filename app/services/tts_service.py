import os
import subprocess
from datetime import datetime

from app.config import ESPEAK_PATH, ESPEAK_DATA_PATH

TTS_OUTPUT_DIR = os.path.join("storage", "audio_output")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)

VOICE_CODES = {
    "en": {
        "male": "en+m3",
        "female": "en+f3"
    },
    "hi": {
        "male": "hi+m3",
        "female": "hi+f3"
    },
    "mr": {
        "male": "mr+m3",
        "female": "mr+f3"
    }
}


def generate_speech(text: str, target_language: str, voice_gender: str = "male") -> str:
    if target_language not in VOICE_CODES:
        raise ValueError(f"Unsupported TTS language: {target_language}")

    if voice_gender not in VOICE_CODES[target_language]:
        raise ValueError(f"Unsupported voice gender: {voice_gender}")

    voice_code = VOICE_CODES[target_language][voice_gender]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    input_text_path = os.path.join(
        TTS_OUTPUT_DIR,
        f"tts_input_{timestamp}.txt"
    )
    output_audio_path = os.path.join(
        TTS_OUTPUT_DIR,
        f"translated_audio_{timestamp}.wav"
    )

    with open(input_text_path, "w", encoding="utf-8") as file:
        file.write(text)

    command = [
        ESPEAK_PATH,
        "-v", voice_code,
        "--path", ESPEAK_DATA_PATH,
        "-w", output_audio_path,
        "-f", input_text_path
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
