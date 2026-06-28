import torch
import numpy as np
from PIL import Image

from app.models import load_model
from app.config import DEVICE


class BackgroundRemover:

    def __init__(self):
        self.model = None

    def load(self):
        self.model = load_model(DEVICE)
        self.model = self.model.to(DEVICE)

        if DEVICE == "cuda":
            self.model = self.model.half()
        else:
            self.model = self.model.float()

        self.dtype = next(self.model.parameters()).dtype

    # ---------- PREPROCESS ----------
    def preprocess(self, image: Image.Image):
        image = image.convert("RGB")

        img = np.array(image).astype(np.float32) / 255.0
        img = torch.from_numpy(img).permute(2, 0, 1)  # CHW
        img = img.unsqueeze(0)  # BCHW

        return img.to(DEVICE, dtype=self.dtype)

    # ---------- INFERENCE ----------
    @torch.inference_mode()
    def infer(self, tensor):
        output = self.model(tensor)

        # BiRefNet обычно возвращает:
        # - tensor
        # - dict
        # - или object с logits
        if isinstance(output, dict):
            pred = output.get("logits", list(output.values())[0])
        elif isinstance(output, (list, tuple)):
            pred = output[0]
        else:
            pred = output

        # приводим к вероятностям
        mask = torch.sigmoid(pred)

        # берем первый канал/батч
        mask = mask[0][0].detach().cpu().numpy()

        return mask

    # ---------- POSTPROCESS ----------
    def postprocess(self, mask, image: Image.Image):
        image = image.convert("RGBA")

        mask = (mask * 255).astype(np.uint8)

        mask_img = Image.fromarray(mask).resize(image.size)

        rgba = image.copy()
        rgba.putalpha(mask_img)

        return rgba

    # ---------- PIPE ----------
    def remove_background(self, image: Image.Image):
        tensor = self.preprocess(image)
        mask = self.infer(tensor)
        result = self.postprocess(mask, image)

        return result