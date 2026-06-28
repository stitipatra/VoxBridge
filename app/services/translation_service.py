from app.ai.translation_manager import get_translation_model

LANGUAGE_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "mr": "mar_Deva"
}


def translate_text(text: str, source_language: str, target_language: str) -> str:
    if source_language == target_language:
        return text

    if source_language == "auto":
        raise ValueError(
            "Auto source language should be resolved before translation")

    if source_language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported source language: {source_language}")

    if target_language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported target language: {target_language}")

    tokenizer, model = get_translation_model()

    tokenizer.src_lang = LANGUAGE_CODES[source_language]

    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    )

    forced_bos_token_id = tokenizer.convert_tokens_to_ids(
        LANGUAGE_CODES[target_language]
    )

    output_tokens = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=512
    )

    translated_text = tokenizer.batch_decode(
        output_tokens,
        skip_special_tokens=True
    )[0]

    return translated_text
