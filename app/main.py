from contextlib import asynccontextmanager
from io import BytesIO

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image

from app.inference import BackgroundRemover
from app.logger import setup_logger

logger = setup_logger()

remover = BackgroundRemover()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting service...")
    remover.load()
    logger.info("Service ready")
    yield
    logger.info("Shutdown")


app = FastAPI(
    title="Background Removal API",
    version="1.0",
    lifespan=lifespan
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": remover.model is not None
            }


@app.post(
"/remove-background",
    summary="Remove image background",
    description="Returns PNG with transparent background using BiRefNet"
)
async def remove_background(file: UploadFile = File(...)):


    if file.content_type not in ["image/png", "image/jpeg"]:
        raise HTTPException(status_code=400, detail="Invalid image type")

    image = Image.open(file.file)

    if image.width > 4000 or image.height > 4000:
        raise HTTPException(status_code=400, detail="Image too large")

    result = remover.remove_background(image)

    buffer = BytesIO()
    result.save(buffer, format="PNG")
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="image/png")