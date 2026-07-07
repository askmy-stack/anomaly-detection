# anomaly-detection

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Anomaly detection research repository evolving from vision-based crime classification experiments into a unified tabular and time-series framework.

## Current state

**What exists today**

- Jupyter notebooks for image and video anomaly detection (TensorFlow/Keras SavedModels)
- Pre-trained model artifacts under `Image Anomaly Detection-1/`, `Image Anomaly Detection-2/`, and `Video Anomaly Detection/`
- Legacy static HTML frontend (deprecated) under `examples/legacy-frontend/`

**In progress**

- Python package skeleton at `src/anomaly_detection/` for config, ingestion, preprocessing, models, evaluation, API, and CLI
- Roadmap and phased execution plan in [docs/EXECUTION_PLAN.md](docs/EXECUTION_PLAN.md)

The README previously described a finished tabular ML pipeline; that work is planned for Phases 2–4. This document reflects the repository as it stands after Phase 1 foundation work.

## Project layout

```
src/anomaly_detection/   # installable package (skeleton)
configs/                 # YAML configuration
examples/notebooks/      # relocated vision notebooks
examples/legacy-frontend/  # deprecated static site
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

Verify the install:

```bash
pytest tests/ -q
ruff check src tests
detect   # prints stub message until Phase 3
```

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
