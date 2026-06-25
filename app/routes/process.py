from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from app.services.translation_service import translate_text
from app.services.output_service import save_text_output

router = APIRouter(prefix="/process", tags=["Process"])


class ProcessRequest(BaseModel):
    input_type: str
    input_path: str
    source_language: str
    target_language: str


@router.post("/")
def process_file(request: ProcessRequest):
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
