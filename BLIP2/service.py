from __future__ import annotations

import typing as t

import bentoml
import logging
from PIL.Image import Image

logger = logging.getLogger(__name__)

MODEL_ID = "Salesforce/blip2-opt-2.7b"


@bentoml.service(
    resources={
        "gpu": 1,
        "gpu_type": "nvidia-tesla-a100",
    }
)
class BlipImageCaptioning:
    hf_model = bentoml.models.HuggingFaceModel(MODEL_ID)

    def __init__(self) -> None:
        import torch
        from transformers import Blip2Processor, Blip2ForConditionalGeneration

        if torch.cuda.is_available():
            self.device = "cuda"
            self.dtype = torch.float16
        else:
            self.device = "cpu"
            self.dtype = torch.bfloat16

        self.processor = Blip2Processor.from_pretrained(self.hf_model)
        self.model = Blip2ForConditionalGeneration.from_pretrained(
            self.hf_model,
            torch_dtype=self.dtype,
        ).to(self.device)

        logger.info(f"Model '{MODEL_ID}' loaded on device: f{self.device}")

    @bentoml.api
    async def generate(self, img: Image, question: t.Optional[str] = None) -> str:
        img = img.convert("RGB")
        if question:
            inputs = self.processor(img, question, return_tensors="pt").to(
                self.device, self.dtype
            )
        else:
            inputs = self.processor(img, return_tensors="pt").to(
                self.device, self.dtype
            )

        print("inputs:", inputs)
        out = self.model.generate(**inputs, max_new_tokens=100)
        print("output:", out)
        res = self.processor.decode(out[0], skip_special_tokens=True).strip()
        print("res:", res)
        return res
