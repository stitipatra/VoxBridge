import os
import subprocess
from datetime import datetime

from app.config import ESPEAK_PATH, ESPEAK_DATA_PATH, PIPER_PATH

TTS_OUTPUT_DIR = os.path.join("storage", "audio_output")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)

PIPER_MODELS = {
    "en": {
        "male": os.path.join("models", "en_US-hfc_male-medium.onnx"),
        "female": os.path.join("models", "en_US-lessac-medium.onnx"),
    },
    "hi": {
        "male": os.path.join("models", "hi_IN-rohan-medium.onnx"),
        "female": os.path.join("models", "hi_IN-priyamvada-medium.onnx"),
    },
}

ESPEAK_VOICE_CODES = {
    "mr": {
        "male": "mr+m3",
        "female": "mr+f3",
    }
}


def generate_speech(
    text: str,
    target_language: str,
    voice_gender: str = "male",
) -> str:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

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

    if target_language in PIPER_MODELS:
        _generate_with_piper(
            input_text_path,
            output_audio_path,
            target_language,
            voice_gender
        )

    elif target_language in ESPEAK_VOICE_CODES:
        _generate_with_espeak(
            input_text_path,
            output_audio_path,
            target_language,
            voice_gender
        )

    else:
        raise ValueError(
            f"Unsupported language: {target_language}"
        )

    return output_audio_path


def _generate_with_piper(
    input_text_path,
    output_audio_path,
    target_language,
    voice_gender,
):

    if voice_gender not in PIPER_MODELS[target_language]:
        raise ValueError(
            f"Unsupported voice gender: {voice_gender}"
        )

    model_path = PIPER_MODELS[target_language][voice_gender]

    if not os.path.exists(model_path):
        raise FileNotFoundError(model_path)

    command = [
        PIPER_PATH,
        "--model",
        model_path,
        "--input-file",
        input_text_path,
        "--output-file",
        output_audio_path,
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)


def _generate_with_espeak(
    input_text_path,
    output_audio_path,
    target_language,
    voice_gender,
):

    voice_code = ESPEAK_VOICE_CODES[target_language][voice_gender]

    command = [
        ESPEAK_PATH,
        "-v",
        voice_code,
        "--path",
        ESPEAK_DATA_PATH,
        "-w",
        output_audio_path,
        "-f",
        input_text_path,
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)
