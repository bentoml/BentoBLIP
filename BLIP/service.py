from __future__ import annotations

import typing as t

import bentoml
from PIL.Image import Image

MODEL_ID = "Salesforce/blip-image-captioning-large"

@bentoml.service(
    resources={
        "gpu": 1,
    }
)
class BlipImageCaptioning:    
    
    def __init__(self) -> None:
        import torch
        from transformers import BlipProcessor, BlipForConditionalGeneration

        # self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if torch.cuda.is_available():
            self.device = "cuda"
            self.dtype = torch.float16
        else:
            self.device = "cpu"
            self.dtype = torch.bfloat16

        self.model = BlipForConditionalGeneration.from_pretrained(MODEL_ID).to(self.device)
        self.processor = BlipProcessor.from_pretrained(MODEL_ID)
        print("Model blip loaded", "device:", self.device)
    
    @bentoml.api(batchable=True)
    async def generate(
        self,
        image: Image,
        text: t.Optional[str] = None
    ) -> str:
        image = image.convert("RGB")
        if text:
            # conditional image captioning
            inputs = self.processor(image, text, return_tensors="pt").to(self.device, self.dtype)
        else:
            # unconditional image captioning
            inputs = self.processor(image, return_tensors="pt").to(self.device, self.dtype)

        out = self.model.generate(**inputs, max_new_tokens=100, min_new_tokens=20)
        return self.processor.decode(out[0], skip_special_tokens=True)
