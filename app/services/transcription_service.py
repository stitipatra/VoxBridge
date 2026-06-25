import os
from datetime import datetime

from app.ai.model_manager import get_whisper_model

TRANSCRIPT_DIR = os.path.join("storage", "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def transcribe_audio(audio_path: str, source_language: str = "en") -> dict:
    model = get_whisper_model()

    segments, info = model.transcribe(
        audio_path,
        language=source_language,
        beam_size=5
    )

    transcript_parts = []
    timed_segments = []

    for segment in segments:
        text = segment.text.strip()

        transcript_parts.append(text)
        timed_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": text
        })

    transcript_text = " ".join(transcript_parts)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    transcript_path = os.path.join(
        TRANSCRIPT_DIR,
        f"transcript_{timestamp}.txt"
    )

    with open(transcript_path, "w", encoding="utf-8") as file:
        file.write(transcript_text)

    return {
        "detected_language": info.language,
        "duration": info.duration,
        "transcript_text": transcript_text,
        "segments": timed_segments,
        "transcript_path": transcript_path
    }
