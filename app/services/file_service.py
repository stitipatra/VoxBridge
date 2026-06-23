# app/services/file_service.py
import os
import shutil
from fastapi import UploadFile

BASE_STORAGE_DIR = "storage"

TEXT_UPLOAD_DIR = os.path.join(BASE_STORAGE_DIR, "uploads", "text")
AUDIO_UPLOAD_DIR = os.path.join(BASE_STORAGE_DIR, "uploads", "audio")
VIDEO_UPLOAD_DIR = os.path.join(BASE_STORAGE_DIR, "uploads", "video")

TEXT_EXTENSIONS = {".txt"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".aac", ".m4a", ".flac", ".wma", ".ogg"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".wmv", ".mkv", ".flv", ".webm"}

for directory in [TEXT_UPLOAD_DIR, AUDIO_UPLOAD_DIR, VIDEO_UPLOAD_DIR]:
    os.makedirs(directory, exist_ok=True)


def detect_file_type(filename: str) -> str:
    _, ext = os.path.splitext(filename.lower())

    if ext in TEXT_EXTENSIONS:
        return "text"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in VIDEO_EXTENSIONS:
        return "video"

    return "unsupported"


def get_upload_directory(file_type: str) -> str:
    if file_type == "text":
        return TEXT_UPLOAD_DIR
    if file_type == "audio":
        return AUDIO_UPLOAD_DIR
    if file_type == "video":
        return VIDEO_UPLOAD_DIR

    raise ValueError("Unsupported file type")


async def save_upload_file(file: UploadFile) -> str:
    file_type = detect_file_type(file.filename)
    upload_dir = get_upload_directory(file_type)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path
