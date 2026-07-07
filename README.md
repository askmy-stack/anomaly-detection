# anomaly-detection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Anomaly detection research repository evolving from vision-based crime classification experiments into a unified tabular and time-series framework.

## Current state

**What exists today**

- Jupyter notebooks for image and video anomaly detection (TensorFlow/Keras SavedModels)
- Pre-trained model artifacts at the repository root:
  - `Image Anomaly Detection-2/` — image classifier SavedModel
  - `Video Anomaly Detection/` — video classifier SavedModel
  - `Image Anomaly Detection-1/` — legacy image model
- Vision domain module at `src/anomaly_detection/domains/vision/` (Phase 7)
- Legacy static HTML frontend (deprecated) under `examples/legacy-frontend/`

**Important:** The UCF vision module performs **supervised multi-class classification** (14 crime categories). It is not unsupervised anomaly detection and should not be conflated with the tabular `/detect` API.

**In progress**

- Python package at `src/anomaly_detection/` for config, ingestion, preprocessing, models, evaluation, API, and CLI
- Roadmap and phased execution plan in [docs/EXECUTION_PLAN.md](docs/EXECUTION_PLAN.md)

## Project layout

```
src/anomaly_detection/   # installable package
  domains/vision/      # UCF image/video classification (optional [vision] extra)
configs/                 # YAML configuration
  examples/vision.yaml   # vision model paths and settings
examples/notebooks/      # relocated vision notebooks
examples/legacy-frontend/  # deprecated static site
Image Anomaly Detection-2/   # image SavedModel (not in git LFS by default)
Video Anomaly Detection/     # video SavedModel
tests/                   # pytest suite
docs/                    # execution plan and design docs
datasets/                # dataset registry (Phase 4)
```

## Setup

Requires Python 3.11+.

```bash
git clone https://github.com/askmy-stack/anomaly-detection.git
cd anomaly-detection
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Optional: vision classification

Install TensorFlow and OpenCV for UCF image/video endpoints:

```bash
pip install -e ".[dev,vision]"
```

Model paths are configured in `configs/examples/vision.yaml` (defaults point to SavedModels at repo root).

Verify the install:

```bash
pytest tests/ -q
ruff check src tests
detect   # tabular CLI
serve    # REST API (includes /vision/analyze/* when [vision] installed)
```

Vision API endpoints (require `[vision]` extra):

- `POST /vision/analyze/image` — classify a single image
- `POST /vision/analyze/video` — classify a video (sync frame sampling)

To explore the original vision notebooks:

```bash
jupyter notebook examples/notebooks/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please read [docs/EXECUTION_PLAN.md](docs/EXECUTION_PLAN.md) before starting substantial work.

## License

MIT — see [LICENSE](LICENSE).

---

Built by [Abhinaysai Kamineni](https://github.com/askmy-stack)
