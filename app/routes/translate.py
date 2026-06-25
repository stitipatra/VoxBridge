from pydantic import BaseModel
from fastapi import APIRouter
from app.services.translation_service import translate_text
from app.services.output_service import save_text_output

router = APIRouter(prefix="/translate", tags=["Translation"])


class TextTranslationRequest(BaseModel):
    text: str
    source_language: str
    target_language: str


@router.post("/text")
def translate_text_endpoint(request: TextTranslationRequest):
    translated_text = translate_text(
        request.text,
        request.source_language,
        request.target_language
    )

    saved_path = save_text_output(translated_text, "translation")

    return {
        "source_language": request.source_language,
        "target_language": request.target_language,
        "original_text": request.text,
        "translated_text": translated_text,
        "saved_path": saved_path
    }
