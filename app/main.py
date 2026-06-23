from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.files import router as files_router

app = FastAPI(title="VoxBridge")

app.include_router(upload_router, prefix="/api")
app.include_router(files_router, prefix="/api")


@app.get("/")
def root():
    return {"project": "VoxBridge", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
