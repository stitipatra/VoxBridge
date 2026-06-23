from pydantic import BaseModel
from fastapi import APIRouter
from app.services.translation_service import translate_text

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

    return {
        "source_language": request.source_language,
        "target_language": request.target_language,
        "original_text": request.text,
        "translated_text": translated_text
    }
