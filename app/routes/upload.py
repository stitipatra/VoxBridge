# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import save_upload_file, detect_file_type

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    file_type = detect_file_type(file.filename)

    if file_type == "unsupported":
        raise HTTPException(status_code=400, detail="Unsupported file type")

    saved_path = await save_upload_file(file)

    return {
        "filename": file.filename,
        "file_type": file_type,
        "saved_path": saved_path,
        "message": "File uploaded successfully"
    }
