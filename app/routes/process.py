from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.services.translation_service import translate_text
from app.services.output_service import save_text_output
from app.services.media_service import extract_audio_from_video, convert_audio_to_wav
from app.services.transcription_service import transcribe_audio

router = APIRouter(prefix="/process", tags=["Process"])


class ProcessRequest(BaseModel):
    input_type: str
    input_path: str
    source_language: str
    target_language: str


@router.post("/")
def process_file(request: ProcessRequest):

    if request.input_type == "video":
        try:
            audio_path = extract_audio_from_video(request.input_path)
            transcription_result = transcribe_audio(
                audio_path,
                request.source_language
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {
            "message": "Video transcribed successfully",
            "input_type": request.input_type,
            "input_path": request.input_path,
            "audio_output_path": audio_path,
            "detected_language": transcription_result["detected_language"],
            "duration": transcription_result["duration"],
            "transcript_text": transcription_result["transcript_text"],
            "transcript_path": transcription_result["transcript_path"],
            "segments": transcription_result["segments"],
            "status": "completed"
        }

    if request.input_type == "audio":
        try:
            audio_path = convert_audio_to_wav(request.input_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        return {
            "message": "Audio converted successfully",
            "input_type": request.input_type,
            "input_path": request.input_path,
            "audio_output_path": audio_path,
            "status": "completed"
        }

    if request.input_type != "text":
        return {
            "message": "Only text processing is implemented right now",
            "input_type": request.input_type,
            "status": "pending"
        }

    try:
        with open(request.input_path, "r", encoding="utf-8") as file:
            original_text = file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Input file not found")

    translated_text = translate_text(
        original_text,
        request.source_language,
        request.target_language
    )

    saved_path = save_text_output(translated_text, "translation")

    return {
        "message": "Text file processed successfully",
        "input_type": request.input_type,
        "source_language": request.source_language,
        "target_language": request.target_language,
        "input_path": request.input_path,
        "translated_text": translated_text,
        "output_path": saved_path,
        "status": "completed"
    }
