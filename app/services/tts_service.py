import os
import subprocess
from datetime import datetime
from functools import lru_cache
import shutil
import torch
from scipy.io.wavfile import write
from transformers import AutoTokenizer, VitsModel

from app.config import ESPEAK_PATH, ESPEAK_DATA_PATH, PIPER_PATH


TTS_OUTPUT_DIR = os.path.join("storage", "audio_output")
os.makedirs(TTS_OUTPUT_DIR, exist_ok=True)

MARATHI_MMS_MODEL = "facebook/mms-tts-mar"


PIPER_MODELS = {
    "en": {
        "male": os.path.join("models", "en_US-hfc_male-medium.onnx"),
        "female": os.path.join("models", "en_US-amy-medium.onnx"),
    },
    "hi": {
        "male": os.path.join("models", "hi_IN-rohan-medium.onnx"),
        "female": os.path.join("models", "hi_IN-priyamvada-medium.onnx"),
    },
}


ESPEAK_VOICE_CODES = {
    "en": {
        "male": "en+m3",
        "female": "en+f3",
    },
    "hi": {
        "male": "hi+m3",
        "female": "hi+f3",
    },
    "mr": {
        "male": "mr+m3",
        "female": "mr+f3",
    },
}


@lru_cache(maxsize=1)
def _load_marathi_mms():
    """
    Load the Marathi MMS tokenizer and model once per application process.

    Hugging Face also caches the downloaded files on disk, so subsequent
    application launches reuse the local checkpoint instead of downloading it.
    """
    print("Loading Marathi MMS-TTS model...")

    tokenizer = AutoTokenizer.from_pretrained(
        MARATHI_MMS_MODEL,
    )

    model = VitsModel.from_pretrained(
        MARATHI_MMS_MODEL,
    )

    model.eval()

    print("Marathi MMS-TTS model loaded and cached.")

    return tokenizer, model


def generate_speech(
    text: str,
    target_language: str,
    voice_gender: str = "male",
) -> str:

    target_language = target_language.lower().strip()
    voice_gender = voice_gender.lower().strip()

    if voice_gender not in {"male", "female"}:
        raise ValueError(
            f"Unsupported voice gender: {voice_gender}"
        )

    if not text or not text.strip():
        raise ValueError("Cannot generate speech from empty text.")

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    input_text_path = os.path.join(
        TTS_OUTPUT_DIR,
        f"tts_input_{timestamp}.txt",
    )

    output_audio_path = os.path.join(
        TTS_OUTPUT_DIR,
        f"translated_audio_{timestamp}.wav",
    )

    with open(
        input_text_path,
        "w",
        encoding="utf-8",
    ) as file:
        file.write(text.strip())

    if target_language in PIPER_MODELS:
        try:
            _generate_with_piper(
                input_text_path=input_text_path,
                output_audio_path=output_audio_path,
                target_language=target_language,
                voice_gender=voice_gender,
            )

        except Exception as error:
            print(
                f"Piper TTS failed for "
                f"{target_language}/{voice_gender}: {error}"
            )
            print("Falling back to eSpeak.")

            _generate_with_espeak(
                input_text_path=input_text_path,
                output_audio_path=output_audio_path,
                target_language=target_language,
                voice_gender=voice_gender,
            )

    elif target_language == "mr":

        if voice_gender == "female":
            # Keep Marathi female voice on eSpeak.
            _generate_with_espeak(
                input_text_path=input_text_path,
                output_audio_path=output_audio_path,
                target_language=target_language,
                voice_gender=voice_gender,
            )

        else:
            # Marathi male/default voice uses MMS.
            try:
                _generate_with_marathi_mms(
                    text=text,
                    output_audio_path=output_audio_path,
                )

            except Exception as error:
                print(
                    f"Marathi MMS-TTS failed: {error}"
                )
                print(
                    "Falling back to Marathi eSpeak male."
                )

                _generate_with_espeak(
                    input_text_path=input_text_path,
                    output_audio_path=output_audio_path,
                    target_language=target_language,
                    voice_gender="male",
                )

    else:
        raise ValueError(
            f"Unsupported language: {target_language}"
        )

    if not os.path.exists(output_audio_path):
        raise RuntimeError(
            "TTS completed without creating an audio file."
        )

    if os.path.getsize(output_audio_path) == 0:
        raise RuntimeError(
            "TTS created an empty audio file."
        )

    return output_audio_path


def _generate_with_marathi_mms(
    text: str,
    output_audio_path: str,
) -> None:

    tokenizer, model = _load_marathi_mms()

    inputs = tokenizer(
        text.strip(),
        return_tensors="pt",
    )

    with torch.inference_mode():
        waveform = model(
            **inputs
        ).waveform.squeeze()

    audio = waveform.detach().cpu().numpy()

    write(
        output_audio_path,
        rate=model.config.sampling_rate,
        data=audio,
    )


def _generate_with_piper(
    input_text_path: str,
    output_audio_path: str,
    target_language: str,
    voice_gender: str,
) -> None:

    if voice_gender not in PIPER_MODELS[target_language]:
        raise ValueError(
            f"Unsupported voice gender: {voice_gender}"
        )

    model_path = PIPER_MODELS[
        target_language
    ][voice_gender]

    piper_executable = shutil.which(PIPER_PATH)

    if piper_executable is None:
        raise FileNotFoundError(
            f"Piper executable not found: {PIPER_PATH}"
        )

    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Piper model not found: {model_path}"
        )

    command = [
        piper_executable,
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
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or "Piper TTS failed."
        )


def _generate_with_espeak(
    input_text_path: str,
    output_audio_path: str,
    target_language: str,
    voice_gender: str,
) -> None:

    if target_language not in ESPEAK_VOICE_CODES:
        raise ValueError(
            f"No eSpeak voice configured for: "
            f"{target_language}"
        )

    if voice_gender not in ESPEAK_VOICE_CODES[
        target_language
    ]:
        raise ValueError(
            f"No eSpeak {voice_gender} voice configured "
            f"for: {target_language}"
        )

    espeak_executable = shutil.which(ESPEAK_PATH)

    if espeak_executable is None:
        raise FileNotFoundError(
            f"eSpeak executable not found: {ESPEAK_PATH}"
        )

    voice_code = ESPEAK_VOICE_CODES[
        target_language
    ][voice_gender]

    command = [
        espeak_executable,
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
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or "eSpeak TTS failed."
        )
