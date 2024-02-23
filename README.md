<div align="center">
    <h1 align="center">BentoBlip</h1>
    <br>
    <strong>Intelligently link images and words together<br></strong>
    <i>Powered by BentoML 🍱</i>
    <br>
</div>
<br>

BLIP (Bootstrapping Language Image Pre-training) is a technique to improve the way AI models understand and process the relationship between images and textual descriptions.

This project demonstrates how to build an image captioning application on top of a [BLIP model](https://huggingface.co/Salesforce/blip-image-captioning-large) with BentoML.

## Prerequisites

- You have installed Python 3.8+ and `pip`. See the [Python downloads page](https://www.python.org/downloads/) to learn more.
- You have a basic understanding of key concepts in BentoML, such as Services. We recommend you read [Quickstart](https://docs.bentoml.com/en/1.2/get-started/quickstart.html) first.
- (Optional) We recommend you create a virtual environment for dependency isolation for this project. See the [Conda documentation](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) or the [Python documentation](https://docs.python.org/3/library/venv.html) for details.

## Install dependencies

```bash
git clone https://github.com/bentoml/BentoBlip.git
cd BentoBlip
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

The Service is accessible at [http://localhost:3000](http://localhost:3000/). You can interact with it using the Swagger UI or in other different ways:

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

## Deploy to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. [Sign up](https://www.bentoml.com/) if you haven't got a BentoCloud account.

Make sure you have [logged in to BentoCloud](https://docs.bentoml.com/en/latest/bentocloud/how-tos/manage-access-token.html), then run the following command to deploy it.

```bash
bentoml deploy .
```

Once the application is up and running on BentoCloud, you can access it via the exposed URL.

**Note**: For custom deployment in your own infrastructure, use [BentoML to generate an OCI-compliant image](https://docs.bentoml.com/en/latest/guides/containerization.html).
