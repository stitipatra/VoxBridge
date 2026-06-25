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
