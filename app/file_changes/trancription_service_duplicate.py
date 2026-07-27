import os
from datetime import datetime
import re
from collections import Counter
from app.ai.whisper_manager import get_whisper_model

TRANSCRIPT_DIR = os.path.join("storage", "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)


def is_corrupted_segment(text: str) -> bool:
    cleaned = re.sub(r"\s+", "", text)

    if not cleaned:
        return True

    # Reject extreme repeated-character hallucinations such as বববববব...
    character_counts = Counter(cleaned)
    most_common_count = character_counts.most_common(1)[0][1]

    if len(cleaned) >= 20 and most_common_count / len(cleaned) >= 0.65:
        return True

    # Reject very long text with almost no character diversity
    unique_ratio = len(set(cleaned)) / len(cleaned)

    if len(cleaned) >= 40 and unique_ratio < 0.08:
        return True

    return False


def transcribe_audio(audio_path: str, source_language: str = "en") -> dict:
    model = get_whisper_model()

    transcribe_kwargs = {
        "beam_size": 10,
        "temperature": 0.0,
        "condition_on_previous_text": False,
    }

    if source_language != "auto":
        transcribe_kwargs["language"] = source_language

    segments, info = model.transcribe(
        audio_path,
        **transcribe_kwargs
    )

    transcript_parts = []
    timed_segments = []

    for segment in segments:
        text = segment.text.strip()

        if is_corrupted_segment(text):
            print(
                f"Skipping corrupted Whisper segment "
                f"{segment.start:.2f}s–{segment.end:.2f}s: {text[:80]}"
            )
            continue

        transcript_parts.append(text)
        timed_segments.append({
            "start": segment.start,
            "end": segment.end,
            "text": text
        })

    transcript_text = " ".join(transcript_parts)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
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
