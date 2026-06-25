from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.files import router as files_router
from app.routes.translate import router as translate_router
from app.routes.process import router as process_router

app = FastAPI(title="VoxBridge")

app.include_router(upload_router, prefix="/api")
app.include_router(files_router, prefix="/api")
app.include_router(translate_router, prefix="/api")
app.include_router(process_router, prefix="/api")


@app.get("/")
def root():
    return {"project": "VoxBridge", "status": "running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
