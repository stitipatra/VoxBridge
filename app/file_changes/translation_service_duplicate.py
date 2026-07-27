from typing import List

import torch

from app.ai.translation_manager import get_translation_model


LANGUAGE_CODES = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "mr": "mar_Deva",
}


def _validate_languages(
    source_language: str,
    target_language: str,
) -> None:
    """
    Validate source and target languages before translation.
    """

    if source_language == "auto":
        raise ValueError(
            "Auto source language should be resolved before translation"
        )

    if source_language not in LANGUAGE_CODES:
        raise ValueError(
            f"Unsupported source language: {source_language}"
        )

    if target_language not in LANGUAGE_CODES:
        raise ValueError(
            f"Unsupported target language: {target_language}"
        )


def translate_batch(
    texts: List[str],
    source_language: str,
    target_language: str,
) -> List[str]:
    """
    Translate multiple independent text inputs in one model.generate() call.

    Each string remains an independent translation input. The strings are not
    joined together, so one text does not provide context to another text.
    """

    if not texts:
        return []

    if source_language == target_language:
        return texts.copy()

    _validate_languages(
        source_language=source_language,
        target_language=target_language,
    )

    tokenizer, model = get_translation_model()

    tokenizer.src_lang = LANGUAGE_CODES[source_language]

    inputs = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512,
    )

    # Move tokenized inputs to the same device as the model.
    model_device = next(model.parameters()).device

    inputs = {
        name: tensor.to(model_device)
        for name, tensor in inputs.items()
    }

    forced_bos_token_id = tokenizer.convert_tokens_to_ids(
        LANGUAGE_CODES[target_language]
    )

    with torch.inference_mode():
        output_tokens = model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_new_tokens=384,
            num_beams=5,
            repetition_penalty=1.1,
            no_repeat_ngram_size=4,
            length_penalty=1.0,
            early_stopping=True,
        )

    translated_texts = tokenizer.batch_decode(
        output_tokens,
        skip_special_tokens=True,
    )

    return [
        translated_text.strip()
        for translated_text in translated_texts
    ]


def translate_text(
    text: str,
    source_language: str,
    target_language: str,
) -> str:
    """
    Translate one text input.

    This remains available so any other existing parts of the application that
    call translate_text() continue working.
    """

    if source_language == target_language:
        return text

    translated_texts = translate_batch(
        texts=[text],
        source_language=source_language,
        target_language=target_language,
    )

    return translated_texts[0]
