from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.services.translation_service import translate_text
from app.services.output_service import save_text_output
from app.services.media_service import extract_audio_from_video, convert_audio_to_wav
from app.services.transcription_service import transcribe_audio
from app.services.subtitle_service import generate_srt, generate_translated_srt
from app.services.tts_service import generate_speech
from app.services.video_service import merge_audio_with_video

router = APIRouter(prefix="/process", tags=["Process"])


class ProcessRequest(BaseModel):
    input_type: str
    input_path: str
    source_language: str
    target_language: str


def resolve_source_language(requested_language: str, detected_language: str) -> str:
    if requested_language == "auto":
        return detected_language
    return requested_language


def process_speech_input(
    input_type: str,
    input_path: str,
    source_language: str,
    target_language: str
):
    translated_video_path = None

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

    transcription_result = transcribe_audio(
        prepared_audio_path,
        source_language
    )

    resolved_language = resolve_source_language(
        source_language,
        transcription_result["detected_language"]
    )

    translated_text = translate_text(
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

    translated_subtitle_path = generate_translated_srt(
        transcription_result["segments"],
        translated_text,
        translated_subtitle_name
    )

    translated_audio_path = generate_speech(
        translated_text,
        target_language
    )

    if input_type == "video":
        translated_video_path = merge_audio_with_video(
            input_path,
            translated_audio_path
        )

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
        "status": "completed"
    }


@router.post("/")
def process_file(request: ProcessRequest):
    try:
        if request.input_type in {"video", "audio"}:
            return process_speech_input(
                request.input_type,
                request.input_path,
                request.source_language,
                request.target_language
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
            request.target_language
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
