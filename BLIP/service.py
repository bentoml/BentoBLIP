from __future__ import annotations

import typing as t

import bentoml
from PIL.Image import Image

MODEL_ID = "Salesforce/blip-image-captioning-large"

runtime_image = bentoml.images.PythonImage(python_version="3.11")\
                            .requirements_file("requirements.txt")

@bentoml.service(
    image=runtime_image,
    resources={
        "gpu": 1,
        "gpu_type": "nvidia-tesla-t4",
    }
)
class BlipImageCaptioning:
    hf_model = bentoml.models.HuggingFaceModel(MODEL_ID)

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

        self.model = BlipForConditionalGeneration.from_pretrained(self.hf_model).to(
            self.device
        )
        self.processor = BlipProcessor.from_pretrained(self.hf_model)
        print("Model blip loaded", "device:", self.device)

    @bentoml.api
    async def generate(self, img: Image, txt: t.Optional[str] = None) -> str:
        img = img.convert("RGB")
        if txt:
            # conditional image captioning
            inputs = self.processor(img, txt, return_tensors="pt").to(
                self.device, self.dtype
            )
        else:
            # unconditional image captioning
            inputs = self.processor(img, return_tensors="pt").to(
                self.device, self.dtype
            )

        out = self.model.generate(**inputs, max_new_tokens=100, min_new_tokens=20)
        return self.processor.decode(out[0], skip_special_tokens=True)
