from __future__ import annotations

import typing as t

import bentoml
from PIL.Image import Image

MODEL_ID = "Salesforce/blip-image-captioning-large"

@bentoml.service(
    resources={
        "memory" : "4Gi"
    }
)
class BlipImageCaptioning:    
    
    def __init__(self) -> None:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = BlipForConditionalGeneration.from_pretrained(MODEL_ID).to(self.device)
        self.processor = BlipProcessor.from_pretrained(MODEL_ID)
        print("Model blip loaded", "device:", self.device)
    
    @bentoml.api
    async def generate(self, img: Image, txt: t.Optional[str] = None) -> str:
        if txt:
            inputs = self.processor(img, txt, return_tensors="pt").to(self.device)
        else:
            inputs = self.processor(img, return_tensors="pt").to(self.device)

        out = self.model.generate(**inputs, max_new_tokens=100, min_new_tokens=20)
        return self.processor.decode(out[0], skip_special_tokens=True)
