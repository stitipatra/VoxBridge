from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import re
import os
import time
from concurrent.futures import ThreadPoolExecutor
from app.services.translation_service import translate_text
from app.services.output_service import save_text_output
from app.services.media_service import extract_audio_from_video, convert_audio_to_wav
from app.services.transcription_service import transcribe_audio
from app.services.subtitle_service import generate_srt, split_segments_for_subtitles, generate_ass
from app.services.tts_service import generate_speech
from typing import Callable, Optional
from app.services.video_service import (
    merge_audio_with_video,
    get_video_dimensions,
    generate_segment_audio_clips,
    create_synchronized_audio
)

router = APIRouter(prefix="/process", tags=["Process"])


class ProcessRequest(BaseModel):
    input_type: str
    input_path: str
    source_language: str
    target_language: str
    voice_gender: str = "male"


def log_timing(message):
    with open("timing_report.txt", "a", encoding="utf-8") as f:
        f.write(message + "\n")


def resolve_source_language(requested_language: str, detected_language: str) -> str:
    if requested_language == "auto":
        return detected_language
    return requested_language


def translate_segments(
    segments: list,
    source_language: str,
    target_language: str,
    max_chars: int = 300,
    progress_callback=None,
    progress_start=38,
    progress_end=68
) -> list:
    grouped_segments = []
    current_text_parts = []
    current_start = None
    current_end = None

    for segment in segments:
        segment_text = segment["text"].strip()

        if not segment_text:
            continue

        candidate_text = " ".join(current_text_parts + [segment_text])

        if current_text_parts and len(candidate_text) > max_chars:
            grouped_segments.append({
                "start": current_start,
                "end": current_end,
                "text": " ".join(current_text_parts)
            })

            current_text_parts = [segment_text]
            current_start = segment["start"]
            current_end = segment["end"]

        else:
            if current_start is None:
                current_start = segment["start"]

            current_text_parts.append(segment_text)
            current_end = segment["end"]

    if current_text_parts:
        grouped_segments.append({
            "start": current_start,
            "end": current_end,
            "text": " ".join(current_text_parts)
        })

    translated_segments = []

    total_groups = max(len(grouped_segments), 1)

    for index, group in enumerate(grouped_segments):

        translated_text = translate_text(
            group["text"],
            source_language,
            target_language
        ).strip()

        if translated_text:
            translated_segments.append({
                "start": group["start"],
                "end": group["end"],
                "text": translated_text
            })

        if progress_callback:
            completed = index + 1

            progress = progress_start + int(
                completed / total_groups
                * (progress_end - progress_start)
            )

            progress_callback(
                min(progress, progress_end),
                f"Translating content ({completed}/{total_groups})"
            )

    return translated_segments


def create_subtitle_segments_from_translated_text(
    translated_text: str,
    duration: float,
    max_chars: int
) -> list:
    words = translated_text.strip().split()

    if not words:
        return []

    chunks = []
    current_chunk = ""

    for word in words:
        next_chunk = f"{current_chunk} {word}".strip()

        if len(next_chunk) <= max_chars:
            current_chunk = next_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = word

    if current_chunk:
        chunks.append(current_chunk)

    chunk_duration = duration / len(chunks)

    subtitle_segments = []

    for index, chunk in enumerate(chunks):
        subtitle_segments.append({
            "start": index * chunk_duration,
            "end": (index + 1) * chunk_duration,
            "text": chunk
        })

    return subtitle_segments


def process_speech_input(
    input_type: str,
    input_path: str,
    source_language: str,
    target_language: str,
    voice_gender: str,
    progress_callback=None
):
    print(">>> ENTERED process_speech_input <<<", flush=True)

    def report_progress(progress, stage):
        if progress_callback:
            progress_callback(progress, stage)

    report_progress(3, "Preparing uploaded file")
    open("timing_report.txt", "w").close()
    total_start = time.perf_counter()
    stage_timings = {}

    translated_video_path = None

    stage_start = time.perf_counter()

    if input_type == "video":
        prepared_audio_path = extract_audio_from_video(input_path)
        original_subtitle_name = "video_original_subtitles"
        translated_subtitle_name = "video_translated_subtitles"
        translation_output_name = "video_translation"
    elif input_type == "audio":
        prepared_audio_path = convert_audio_to_wav(input_path)
        original_subtitle_name = "audio_original_subtitles"
        translated_subtitle_name = "audio_translated_subtitles"
        translation_output_name = "audio_translation"
    else:
        raise ValueError(f"Unsupported speech input type: {input_type}")

    stage_timings["audio_preparation"] = (
        time.perf_counter() - stage_start
    )

    report_progress(8, "Transcribing speech")

    stage_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=1) as executor:
        transcription_future = executor.submit(
            transcribe_audio,
            prepared_audio_path,
            source_language
        )

        estimated_progress = 8

        while not transcription_future.done():
            elapsed = time.perf_counter() - stage_start

            # Moves quickly at first, then slows down near 35%.
            estimated_progress = min(
                37,
                8 + int(elapsed / 2)
            )

            report_progress(
                estimated_progress,
                "Transcribing speech"
            )

            time.sleep(0.5)

        # Raises the original error if transcription failed.
        transcription_result = transcription_future.result()

    stage_timings["transcription"] = (
        time.perf_counter() - stage_start
    )

    report_progress(38, "Translating content")

    resolved_language = resolve_source_language(
        source_language,
        transcription_result["detected_language"]
    )

    '''translated_text = translate_long_text(
        transcription_result["transcript_text"],
        resolved_language,
        target_language
    )

    translated_text_path = save_text_output(
        translated_text,
        translation_output_name
    )

    original_subtitle_path = generate_srt(
        transcription_result["segments"],
        original_subtitle_name
    )

    #translated_segments = translate_segments(
    #    transcription_result["segments"],
    #    resolved_language,
    #    target_language
    #)

    subtitle_max_chars = {
        "en": 28,
        "hi": 22,
        "mr": 22
    }

    translated_segments = create_subtitle_segments_from_translated_text(
        translated_text,
        transcription_result["duration"],
        subtitle_max_chars.get(target_language, 28)
    )'''

    stage_start = time.perf_counter()

    original_subtitle_path = generate_srt(
        transcription_result["segments"],
        original_subtitle_name
    )

    translated_segments = translate_segments(
        transcription_result["segments"],
        resolved_language,
        target_language,
        progress_callback=progress_callback,
        progress_start=38,
        progress_end=68
    )

    stage_timings["translation"] = (
        time.perf_counter() - stage_start
    )

    stage_start = time.perf_counter()

    translated_text = " ".join(
        segment["text"].strip()
        for segment in translated_segments
        if segment["text"].strip()
    )

    translated_text_path = save_text_output(
        translated_text,
        translation_output_name
    )

    report_progress(72, "Generating subtitles")

    '''translated_subtitle_path = generate_srt(
        translated_segments,
        translated_subtitle_name
    )'''

    if input_type == "video":
        video_width, video_height = get_video_dimensions(input_path)

    else:
        video_width, video_height = 1280, 720

    formatted_segments = split_segments_for_subtitles(
        translated_segments,
        max_line_chars=28
    )

    '''for segment in formatted_segments:
        print(
            f'{segment["start"]:.2f} -> {segment["end"]:.2f} | '
            f'{segment["text"]!r}'
        )'''

    translated_subtitle_path = generate_ass(
        formatted_segments,
        translated_subtitle_name,
        video_width,
        video_height
    )

    stage_timings["subtitle_generation"] = (
        time.perf_counter() - stage_start
    )

    if input_type == "video":

        stage_start = time.perf_counter()

        report_progress(76, "Generating translated voice")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                generate_segment_audio_clips,
                translated_segments,
                target_language,
                voice_gender
            )

            stage_start = time.perf_counter()

            while not future.done():
                elapsed = time.perf_counter() - stage_start

                progress = min(
                    88,
                    76 + int(elapsed / 2)
                )

                report_progress(
                    progress,
                    "Generating translated voice"
                )

                time.sleep(0.5)

            segment_audio_clips = future.result()

        stage_timings["tts_generation"] = (
            time.perf_counter() - stage_start
        )

        report_progress(89, "Synchronizing translated audio")

        stage_start = time.perf_counter()

        translated_audio_path = create_synchronized_audio(segment_audio_clips)

        stage_timings["audio_synchronization"] = (
            time.perf_counter() - stage_start
        )

        stage_start = time.perf_counter()

        report_progress(94, "Rendering final video")

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                merge_audio_with_video,
                input_path,
                translated_audio_path,
                translated_subtitle_path
            )

            stage_start = time.perf_counter()

            while not future.done():
                elapsed = time.perf_counter() - stage_start

                progress = min(
                    98,
                    94 + int(elapsed)
                )

                report_progress(
                    progress,
                    "Rendering final video"
                )

                time.sleep(0.5)

            translated_video_path = future.result()

        stage_timings["video_rendering"] = (
            time.perf_counter() - stage_start
        )

        stage_start = time.perf_counter()

        report_progress(99, "Finalizing output")

        # Cleanup temporary clips
        for clip in segment_audio_clips:
            for temp_path in clip["temporary_paths"]:
                try:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                except OSError:
                    pass
        stage_timings["cleanup"] = (
            time.perf_counter() - stage_start
        )

    else:

        stage_start = time.perf_counter()

        translated_audio_path = generate_speech(
            translated_text,
            target_language,
            voice_gender
        )

        stage_timings["tts_generation"] = (
            time.perf_counter() - stage_start
        )

    total_time = time.perf_counter() - total_start

    log_timing("")

    log_timing("=" * 60)
    log_timing("ANUWADINI PROCESSING TIME REPORT")
    log_timing("=" * 60)

    for stage_name, duration in stage_timings.items():
        percentage = (
            duration / total_time * 100
            if total_time > 0
            else 0
        )

        readable_name = stage_name.replace("_", " ").title()

        log_timing(
            f"{readable_name:<28}"
            f"{duration:>9.2f} sec "
            f"({percentage:>6.2f}%)"
        )

    measured_time = sum(stage_timings.values())
    unmeasured_time = max(0.0, total_time - measured_time)

    log_timing(
        f"{'Unmeasured / Overhead':<28}"
        f"{unmeasured_time:>9.2f} sec "
        f"({(unmeasured_time / total_time * 100) if total_time > 0 else 0:>6.2f}%)"
    )

    log_timing("-" * 60)
    log_timing(f"{'Total':<28}{total_time:>9.2f} sec")
    log_timing("=" * 60)
    log_timing("")

    report_progress(100, "Processing complete")

    return {
        "message": f"{input_type.capitalize()} processed successfully",
        "input_type": input_type,
        "input_path": input_path,
        "audio_output_path": prepared_audio_path,
        "detected_language": transcription_result["detected_language"],
        "resolved_source_language": resolved_language,
        "target_language": target_language,
        "duration": transcription_result["duration"],
        "transcript_text": transcription_result["transcript_text"],
        "translated_text": translated_text,
        "transcript_path": transcription_result["transcript_path"],
        "translated_text_path": translated_text_path,
        "original_subtitle_path": original_subtitle_path,
        "translated_subtitle_path": translated_subtitle_path,
        "translated_audio_path": translated_audio_path,
        "translated_video_path": translated_video_path,
        "segments": transcription_result["segments"],
        "translated_segments": translated_segments,
        "status": "completed"
    }


@router.post("/")
def process_file(request: ProcessRequest, progress_callback=None):
    print("\n>>> PROCESS_FILE STARTED <<<", flush=True)
    try:
        if request.input_type in {"video", "audio"}:
            return process_speech_input(
                request.input_type,
                request.input_path,
                request.source_language,
                request.target_language,
                request.voice_gender,
                progress_callback=progress_callback
            )

        if request.input_type != "text":
            return {
                "message": "Unsupported input type",
                "input_type": request.input_type,
                "status": "failed"
            }

        with open(request.input_path, "r", encoding="utf-8") as file:
            original_text = file.read()

        if request.source_language == "auto":
            raise ValueError(
                "Auto source language is not supported for text files yet")

        translated_text = translate_text(
            original_text,
            request.source_language,
            request.target_language
        )

        translated_text_path = save_text_output(
            translated_text,
            "text_translation"
        )

        translated_audio_path = generate_speech(
            translated_text,
            request.target_language,
            request.voice_gender
        )

        return {
            "message": "Text file translated and converted to speech successfully",
            "input_type": request.input_type,
            "source_language": request.source_language,
            "target_language": request.target_language,
            "input_path": request.input_path,
            "original_text": original_text,
            "translated_text": translated_text,
            "translated_text_path": translated_text_path,
            "translated_audio_path": translated_audio_path,
            "status": "completed"
        }

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Input file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def chunk_text(text: str, max_chars: int = 400) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()

    if not text:
        return []

    # Split after English or Devanagari sentence-ending punctuation.
    sentences = re.split(r"(?<=[.!?।])\s+", text)

    chunks = []
    current_sentences = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        # Handle an abnormally long ASR sentence.
        if len(sentence) > max_chars:
            if current_sentences:
                chunks.append(" ".join(current_sentences))
                current_sentences = []
                current_length = 0

            words = sentence.split()
            word_chunk = []

            for word in words:
                candidate = " ".join(word_chunk + [word])

                if len(candidate) <= max_chars:
                    word_chunk.append(word)
                else:
                    if word_chunk:
                        chunks.append(" ".join(word_chunk))
                    word_chunk = [word]

            if word_chunk:
                chunks.append(" ".join(word_chunk))

            continue

        candidate_length = current_length + len(sentence) + 1

        if current_sentences and candidate_length > max_chars:
            chunks.append(" ".join(current_sentences))
            current_sentences = [sentence]
            current_length = len(sentence)
        else:
            current_sentences.append(sentence)
            current_length = candidate_length

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks


def translate_long_text(
    text: str,
    source_language: str,
    target_language: str
) -> str:
    chunks = chunk_text(text, max_chars=100)

    translated_chunks = []

    for chunk in chunks:
        translated_chunk = translate_text(
            chunk,
            source_language,
            target_language
        )

        if translated_chunk.strip():
            translated_chunks.append(translated_chunk.strip())

    return "\n\n".join(translated_chunks)
