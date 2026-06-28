from transformers import AutoModelForImageSegmentation

from app.config import MODEL_NAME
from app.logger import setup_logger

logger = setup_logger()


def load_model(device: str):
    logger.info(f"Loading model {MODEL_NAME}")

    model = AutoModelForImageSegmentation.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model.to(device)
    model.eval()

    logger.info("Model loaded")

    return model