def translate_text(text: str, source_language: str, target_language: str) -> str:
    if source_language == target_language:
        return text

    return f"[DUMMY TRANSLATION from {source_language} to {target_language}]: {text}"
