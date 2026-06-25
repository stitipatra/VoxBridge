import os
from datetime import datetime

TRANSLATION_DIR = os.path.join("storage", "translations")

os.makedirs(TRANSLATION_DIR, exist_ok=True)


def save_text_output(text: str, output_type: str = "translation") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_type}_{timestamp}.txt"
    file_path = os.path.join(TRANSLATION_DIR, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)

    return file_path
