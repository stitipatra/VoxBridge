import os
from datetime import datetime

SUBTITLE_DIR = os.path.join("storage", "subtitles")
os.makedirs(SUBTITLE_DIR, exist_ok=True)


def format_timestamp(seconds: float) -> str:
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def generate_srt(segments: list, output_name: str = "subtitles") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    subtitle_path = os.path.join(
        SUBTITLE_DIR,
        f"{output_name}_{timestamp}.srt"
    )

    with open(subtitle_path, "w", encoding="utf-8") as file:
        for index, segment in enumerate(segments, start=1):
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"]

            file.write(f"{index}\n")
            file.write(f"{start} --> {end}\n")
            file.write(f"{text}\n\n")

    return subtitle_path


def generate_translated_srt(original_segments: list, translated_text: str, output_name: str = "translated_subtitles") -> str:
    translated_segments = []

    if len(original_segments) == 1:
        translated_segments.append({
            "start": original_segments[0]["start"],
            "end": original_segments[0]["end"],
            "text": translated_text
        })
    else:
        for segment in original_segments:
            translated_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": translated_text
            })

    return generate_srt(translated_segments, output_name)


def split_segment_for_subtitles(segment: dict, max_chars: int = 45) -> list:
    text = segment["text"].strip()
    start = segment["start"]
    end = segment["end"]

    if len(text) <= max_chars:
        return [segment]

    words = text.split()
    chunks = []
    current = ""

    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = f"{current} {word}".strip()
        else:
            chunks.append(current)
            current = word

    if current:
        chunks.append(current)

    duration = end - start
    chunk_duration = duration / len(chunks)

    split_segments = []

    for index, chunk in enumerate(chunks):
        split_segments.append({
            "start": start + index * chunk_duration,
            "end": start + (index + 1) * chunk_duration,
            "text": chunk
        })

    return split_segments


def split_segments_for_subtitles(segments: list, max_chars: int = 45) -> list:
    final_segments = []

    for segment in segments:
        final_segments.extend(
            split_segment_for_subtitles(segment, max_chars)
        )

    return final_segments
