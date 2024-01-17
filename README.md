BLIP (Bootstrapping Language Image Pre-training) is a technique to improve the way AI models understand and process the relationship between images and textual descriptions. It has a variety of use cases in the AI field, particularly in applications that require a nuanced understanding of both visual and textual data, such as image captioning, visual question answering (VQA), and image-text matching. This repository demonstrates how to build an image captioning application on top of a BLIP model with BentoML.

## **Prerequisites**

- You have installed Python 3.8+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/latest/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See Installation for details.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py`. Run `bentoml serve` in your project directory to start the Service.

```bash
$ bentoml serve .

2024-01-02T08:32:34+0000 [INFO] [cli] Prometheus metrics for HTTP BentoServer from "service:BlipImageCaptioning" can be accessed at http://localhost:3000/metrics.
2024-01-02T08:32:35+0000 [INFO] [cli] Starting production HTTP BentoServer from "service:BlipImageCaptioning" listening on http://localhost:3000 (Press CTRL+C to quit)
Model blip loaded device: cuda
```

Access the Service UI at [http://0.0.0.0:3000](http://0.0.0.0:3000/). You can interact with it using Swagger UI or in other different ways:

CURL

```bash
curl -s -X POST \
    -F txt='unicorn at sunset' \
    -F 'img=@demo.jpg' \
    http://localhost:3000/generate
```

Python client

```python
import bentoml
from pathlib import Path

with bentoml.SyncHTTPClient("http://localhost:3000") as client:
    result = client.generate(
        img=Path("demo.jpg"),
        txt="unicorn at sunset",
    )
```

Expected output:

```bash
unicorn at sunset by a pond with a beautiful landscape in the background, with a reflection of the sun in the water
```

## Deploy the application to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. A configuration YAML file (`bentofile.yaml`) is used to define the build options for your application. It is used for packaging your application into a Bento. See [Bento build options](https://docs.bentoml.com/en/latest/concepts/bento.html#bento-build-options) to learn more.

Make sure you have logged in to BentoCloud, then run the following command in your project directory to deploy the application to BentoCloud. Under the hood, this commands automatically builds a Bento, push the Bento to BentoCloud, and deploy it on BentoCloud.

```bash
bentoml deploy .
```

**Note**: Alternatively, you can manually build the Bento, containerize the Bento as a Docker image, and deploy it in any Docker-compatible environment. See [Docker deployment](https://docs.bentoml.org/en/latest/concepts/deploy.html#docker) for details.

Once the application is up and running on BentoCloud, you can access it via the exposed URL.
