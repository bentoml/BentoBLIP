import bentoml
# Save model to BentoML local model store
if __name__ == "__main__":
    try:
        bentoml.models.get("blip-image-captioning")
        print("Model already exists")
    except:
        import huggingface_hub
        with bentoml.models.create(
            "blip-image-captioning",
        ) as model_ref:
            huggingface_hub.snapshot_download("Salesforce/blip-image-captioning-large", local_dir=model_ref.path, local_dir_use_symlinks=False)
            print(f"Model saved: {model_ref}")