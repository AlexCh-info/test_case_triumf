from pathlib import Path
import torch

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

MODEL_NAME = "ZhengPeng7/BiRefNet"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"