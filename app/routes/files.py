import os
from fastapi import APIRouter

router = APIRouter(prefix="/files", tags=["Files"])


@router.get("/")
def list_files():
    stored_files = []

    for root, dirs, files in os.walk("storage"):
        for file in files:
            stored_files.append(os.path.join(root, file))

    return {
        "count": len(stored_files),
        "files": stored_files
    }
