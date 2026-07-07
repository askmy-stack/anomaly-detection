# Anomaly-Detection Repository — Executable Execution Plan

> **Purpose:** LLM-friendly, phase-by-phase plan to evolve [askmy-stack/anomaly-detection](https://github.com/askmy-stack/anomaly-detection) from a notebook prototype into a modular, community-ready anomaly-detection framework.
>
> **Last updated:** 2026-07-07  
> **Repo path (local):** `/Users/abhinaysaikamineni/gh-cleanup/anomaly-detection`  
> **Discovery source:** [Anomaly-detection repo discovery](afd3d216-9db5-4adf-b6d7-8ae683cd9636)

Each phase is **self-contained** — paste one phase into a new chat and execute without prior context.

---

## Strategic Context (read once)

| Reality today (`main`) | Roadmap target |
|---|---|
| 3 Jupyter notebooks (UCF Crime **multiclass classification**, not unsupervised AD) | General-purpose anomaly-detection framework |
| Static HTML frontend (`Front End Web Pages/`) with broken `submit.php` reference | CLI + FastAPI + optional web UI |
| No `.py`, no `requirements.txt`, no tests, no CI | Modular Python package, CI/CD, tests |
| README claims tabular baselines (z-score, IQR, IF, OCSVM, AE) that **do not exist** | Implemented baselines + honest docs |
| SavedModel artifacts in `Image Anomaly Detection-*` / `Video Anomaly Detection/` | Preserved as `examples/vision/` domain module |
| Open [PR #1](https://github.com/askmy-stack/anomaly-detection/pull/1) (FastAPI + Next.js crime tip-off platform, **CI failing**, unmerged) | Decision required: extract patterns vs. merge wholesale |

**Critical fork (Phase 1.0):** PR #1 solves a *different product* (crime tip-off web app). This plan **extracts reusable patterns** (FastAPI bootstrap, CI layout, training script) into a new framework layout rather than merging PR #1 as-is.

---

## Phase 0: Documentation Discovery (COMPLETED)

### Allowed APIs & Frameworks (verified sources)

| Library | Use | Docs |
|---|---|---|
| **scikit-learn** | `IsolationForest`, `LocalOutlierFactor`, `OneClassSVM`, `StandardScaler` | https://scikit-learn.org/stable/modules/outlier_detection.html |
| **PyOD** | Extended outlier detectors, unified `fit`/`decision_function` | https://pyod.readthedocs.io/ |
| **dtaianomaly** | Benchmark runner patterns, detector interface inspiration | https://dtaianomaly.readthedocs.io/ |
| **Orion** | Time-series AD interface (`fit`/`detect`) inspiration | https://orion.readthedocs.io/ |
| **PySAD** | Streaming / online AD | https://pysad.readthedocs.io/ |
| **PyRCA** | Root-cause analysis, causal graphs | https://pyrca.readthedocs.io/ |
| **AIF360** | Fairness metrics & mitigation | https://aif360.readthedocs.io/ |
| **FastAPI** | REST API (`/detect`, `/health`) | https://fastapi.tiangolo.com/ |
| **Hydra / OmegaConf** | YAML config | https://hydra.cc/docs/intro/ |
| **TensorFlow/Keras** | Vision autoencoders (migrate from notebooks) | Existing notebooks in repo |

### Anti-patterns to avoid

- Do **not** claim tabular baselines exist until `src/anomaly_detection/models/` implements them.
- Do **not** merge PR #1 wholesale — it targets crime tip-off UX, not a detector framework.
- Do **not** commit large `.pb` model binaries to new package paths; use Git LFS or download scripts.
- Do **not** invent detector methods; inherit from a single `BaseDetector` ABC.
- Do **not** use `submit.php` — it does not exist.

### Copy-ready sources in this repo

| Pattern | Location |
|---|---|
| DenseNet121 head | `Video Anomaly Detection/video-anomaly-detection (1).ipynb` cell 16 |
| Conv2D baseline | `Image Anomaly Detection-1/image-anomaly-detection.ipynb` cell 10 |
| UCF labels & hyperparams | Video notebook cell 5; Image-2 notebook cell 0 |
| Frame extraction (OpenCV) | Image notebooks cell 0 |
| Multiclass ROC-AUC | Video notebook cell 20 |
| FastAPI bootstrap (PR branch) | `backend/app/main.py` on `claude/add-claude-documentation-T2cVn` |
| CI pipeline (PR branch) | `.github/workflows/ci.yml` on PR branch |
| Training CLI (PR branch) | `scripts/train.py` on PR branch |

---

## Phase 1: Foundation — Clean-up, Package Layout, Honest Docs

**Goal:** Runnable Python package skeleton, aligned README, governance files, CI green on lint+test.

### 1.1 Restructure directories

Create this layout (move, don't delete notebooks yet):

```
anomaly-detection/
├── src/anomaly_detection/
│   ├── __init__.py
│   ├── config/           # YAML loading
│   ├── data_ingestion/   # loaders, registry
│   ├── preprocessing/    # scaling, windowing
│   ├── models/           # detectors (Phase 2)
│   ├── evaluation/       # metrics, reports
│   ├── api/              # FastAPI app (Phase 3)
│   └── cli/              # detect.py entrypoint (Phase 3)
├── configs/
│   ├── default.yaml
│   └── examples/
├── tests/
├── examples/
│   ├── notebooks/        # move existing .ipynb here
│   └── vision/           # symlink or move SavedModel dirs
├── docs/
├── datasets/
│   └── registry.yaml     # Phase 4
├── pyproject.toml
├── requirements.txt
├── LICENSE
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
└── README.md
```

**Tasks:**
1. `git mv` notebooks → `examples/notebooks/`
2. `git mv` `Front End Web Pages/` → `examples/legacy-frontend/` (mark deprecated in README)
3. Add `pyproject.toml` with `[project.scripts] detect = "anomaly_detection.cli.detect:main"`
4. Add `requirements.txt` with pinned core deps: `numpy`, `pandas`, `scikit-learn`, `pyyaml`, `matplotlib`, `fastapi`, `uvicorn`, `pytest`, `ruff`

**Copy from:** PR branch `backend/pyproject.toml` ruff/pytest/mypy sections.

### 1.2 Fix README to match reality

Replace aspirational claims with:
- **Current:** vision crime-classification notebooks + SavedModels
- **In progress:** tabular/time-series framework (link to this plan)
- Working setup commands that actually work (`pip install -e ".[dev]"`)

### 1.3 Governance files

| File | Action |
|---|---|
| `LICENSE` | Add MIT (README already claims MIT; GitHub shows undeclared) |
| `CODE_OF_CONDUCT.md` | Contributor Covenant v2.1 |
| `CONTRIBUTING.md` | Fork → branch → PR → CI must pass |
| `.gitignore` | `__pycache__/`, `.venv/`, `data/raw/`, `*.pb` (or use LFS) |

### 1.4 CI/CD bootstrap

**Copy from:** PR branch `.github/workflows/ci.yml` — simplify to:
- `ruff check src tests`
- `pytest tests/ -q`
- Drop Netlify/Docker until Phase 3

### Verification checklist

- [ ] `pip install -e ".[dev]"` succeeds
- [ ] `pytest` runs (even if only smoke tests)
- [ ] `ruff check` passes
- [ ] README setup steps work on clean venv
- [ ] `git grep -i "submit.php"` returns nothing in active paths
- [ ] GitHub license badge shows MIT

### Anti-pattern guards

- Do not add detector logic in Phase 1 — skeleton only.
- Do not rewrite notebooks; relocate only.

---

## Phase 2: Unified Detector API & Baseline Algorithms

**Goal:** Pluggable detectors with `fit()`, `score()`, `predict()` for tabular/time-series data.

### 2.1 Base interface

**Copy pattern from:** scikit-learn `BaseEstimator` + Orion's `fit`/`detect` naming.

Create `src/anomaly_detection/models/base.py`:

```python
class BaseDetector(ABC):
    def fit(self, X: np.ndarray) -> "BaseDetector": ...
    def score(self, X: np.ndarray) -> np.ndarray: ...      # higher = more anomalous
    def predict(self, X: np.ndarray) -> np.ndarray: ...    # 0=normal, 1=anomaly
    def fit_predict(self, X: np.ndarray) -> np.ndarray: ...
```

### 2.2 Implement baselines

| Detector | Module | Backend |
|---|---|---|
| Z-score | `models/statistical/zscore.py` | numpy |
| IQR | `models/statistical/iqr.py` | numpy |
| Isolation Forest | `models/ml/isolation_forest.py` | `sklearn.ensemble.IsolationForest` |
| LOF | `models/ml/lof.py` | `sklearn.neighbors.LocalOutlierFactor` |
| One-Class SVM | `models/ml/ocsvm.py` | `sklearn.svm.OneClassSVM` |
| Autoencoder | `models/deep/autoencoder.py` | PyTorch or Keras (match notebook stack) |

**Copy DenseNet/autoencoder patterns from:** `Image Anomaly Detection-2/image-anomaly-detection-2.ipynb` for Keras autoencoder variant.

### 2.3 Configuration-driven runs

Create `configs/default.yaml`:

```yaml
dataset:
  path: data/sample.csv
  target_column: label        # optional, for eval only
preprocessing:
  scaler: standard
model:
  name: isolation_forest
  params:
    contamination: 0.05
    random_state: 42
output:
  report_path: reports/run.json
  plot_path: reports/anomalies.png
```

Create `src/anomaly_detection/config/loader.py` using `yaml.safe_load`.

### 2.4 Factory registry

`src/anomaly_detection/models/registry.py` — map `config.model.name` → class (dict registry, not dynamic import magic).

### Verification checklist

- [ ] Each detector has unit test with synthetic data (inject 5% outliers)
- [ ] `fit` → `score` → `predict` round-trip on 2D array
- [ ] Config YAML switches between z-score and isolation_forest without code edits
- [ ] `pytest tests/models/` all green

### Anti-pattern guards

- Do not wrap sklearn with different method names; keep `fit`/`predict` consistent.
- Do not hardcode dataset paths outside config.

---

## Phase 3: CLI & REST API

**Goal:** `python -m anomaly_detection.cli.detect --config configs/default.yaml` and FastAPI service.

### 3.1 CLI

Create `src/anomaly_detection/cli/detect.py`:
- argparse: `--config`, `--output`, `--verbose`
- Load config → ingest → preprocess → fit → predict → write report JSON + optional plot

### 3.2 FastAPI service

**Copy from:** PR branch `backend/app/main.py` (lifespan, CORS, health) and `backend/app/api/analyze.py` (router pattern).

Create minimal endpoints:

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Liveness |
| `/detect` | POST | Body: `{ "data": [[...]], "config": {...} }` or CSV upload |
| `/detect/batch` | POST | File upload (CSV) |
| `/models` | GET | List registered detectors |

Do **not** port crime-classification `/analyze/image` until Phase 7 (vision domain).

### 3.3 Evaluation integration

`src/anomaly_detection/evaluation/metrics.py`:
- precision, recall, F1, ROC-AUC (when labels available)
- **Copy from:** Video notebook `multiclass_roc_auc_score()` pattern, adapted for binary anomaly labels

### Verification checklist

- [ ] `detect --config configs/default.yaml` exits 0 and writes report
- [ ] `uvicorn anomaly_detection.api.app:app` starts
- [ ] `curl localhost:8000/health` → 200
- [ ] `curl -X POST localhost:8000/detect` with sample payload → scores returned
- [ ] API tests in `tests/api/test_detect.py`

### Anti-pattern guards

- Do not require GPU for tabular API.
- Do not block event loop with long `fit()` — document sync-only for Phase 3; async jobs in Phase 8.

---

## Phase 4: Dataset Registry & Multi-Domain Loaders

**Goal:** Centralized dataset metadata + download/preprocess scripts.

### 4.1 Registry file

Create `datasets/registry.yaml`:

```yaml
datasets:
  - id: credit_card_fraud
    domain: tabular
    source: openml
    url: https://...
    license: CC-BY-4.0
    labeled: true
    description: European card transactions, highly imbalanced

  - id: nab
    domain: timeseries
    source: numenta
    url: https://github.com/numenta/NAB
    license: AGPL-3.0
    labeled: true

  - id: ucf_crime
    domain: vision
    source: kaggle
    local_notebook: examples/notebooks/image-anomaly-detection-2.ipynb
    labeled: true
    description: Multiclass crime video frames (existing repo work)
```

### 4.2 Loader interface

`src/anomaly_detection/data_ingestion/base.py`:

```python
class BaseLoader(ABC):
    def load(self) -> pd.DataFrame: ...
    def metadata(self) -> dict: ...
```

Implement: `loaders/openml_loader.py`, `loaders/csv_loader.py`, `loaders/ucf_loader.py` (wrap existing Kaggle path logic from notebooks).

### 4.3 Benchmark runner

`src/anomaly_detection/evaluation/benchmark.py`:
- Iterate registry × detectors from config
- Output `reports/benchmark_{timestamp}.md` with metrics table
- **Inspiration:** dtaianomaly benchmark runner (do not vendor; replicate interface)

### Verification checklist

- [ ] `python -m anomaly_detection.cli.benchmark --datasets credit_card_fraud` runs
- [ ] Registry validates with JSON Schema or pydantic model
- [ ] UCF loader reads local example without Kaggle mount (mock/small sample)

### Anti-pattern guards

- Do not auto-download large datasets in CI; use cached fixtures in `tests/fixtures/`.
- Document license per dataset in registry.

---

## Phase 5: Streaming & Resource Efficiency (PySAD)

**Goal:** Online anomaly detection for streams with bounded memory.

### 5.1 Streaming interface

Extend `BaseDetector` or add `BaseStreamingDetector`:

```python
class BaseStreamingDetector(ABC):
    def fit_partial(self, x: np.ndarray) -> None: ...
    def score_one(self, x: np.ndarray) -> float: ...
```

### 5.2 PySAD integration

- Add optional dep: `pysad`
- Wrap PySAD streaming estimators in `models/streaming/`
- Implement sliding-window preprocessor: `preprocessing/window.py` (rolling mean, variance, z-score)

### 5.3 Monitoring hooks

`src/anomaly_detection/monitoring/metrics.py`:
- processing rate, latency, memory (psutil)
- Optional Slack webhook alert when `score > threshold`

### Verification checklist

- [ ] Stream 10k synthetic points without OOM
- [ ] Latency p99 < 10ms per point for z-score window (document hardware)
- [ ] `tests/streaming/test_online.py` passes

### Anti-pattern guards

- Do not store full stream history; enforce `max_window` in config.

---

## Phase 6: Root Cause Analysis (PyRCA)

**Goal:** Post-detection causal explanation for multivariate metrics.

### 6.1 RCA module

- Optional dep: `pyrca`
- `src/anomaly_detection/rca/graph.py` — build causal graph from metric DataFrame
- `src/anomaly_detection/rca/scorer.py` — rank root causes for anomaly timestamp

### 6.2 API extension

| Endpoint | Purpose |
|---|---|
| `POST /root_cause` | `{ "anomaly_id", "metrics": {...} }` → ranked causes |
| `GET /root_cause/{id}` | Retrieve cached RCA result |

### 6.3 Visualization

- Export graph as JSON for frontend (Phase 9 dashboard)
- Optional: networkx → pyvis HTML

### Verification checklist

- [ ] RCA runs on synthetic metric chain (A→B→C; inject anomaly at A; B and C flagged)
- [ ] API returns top-3 causes with scores
- [ ] Unit test with mocked PyRCA if dep too heavy for CI

### Anti-pattern guards

- Do not present correlation as causation without disclaimer in API response.

---

## Phase 7: Vision Domain Module (Preserve Existing Work)

**Goal:** Integrate existing UCF crime notebooks/models as `examples/vision/` + optional API.

### 7.1 Extract notebook code to modules

**Copy from:**
- `examples/notebooks/image-anomaly-detection-2.ipynb` → `src/anomaly_detection/domains/vision/densenet.py`
- `examples/notebooks/video-anomaly-detection (1).ipynb` → `domains/vision/video.py`
- PR branch `backend/app/ml/preprocess.py` → `domains/vision/preprocess.py`
- PR branch `backend/app/ml/gradcam.py` → `domains/vision/gradcam.py`

### 7.2 Model artifact strategy

- Move `.pb` files to `models/artifacts/vision/` or document download script
- Add Git LFS tracking for `*.pb`

### 7.3 API (optional)

Port PR branch endpoints as `/vision/analyze/image` and `/vision/analyze/video` — separate from tabular `/detect`.

### Verification checklist

- [ ] `predict_image()` returns 14-class probabilities on test frame
- [ ] Grad-CAM overlay generates without error
- [ ] Model loads from documented path in config

### Anti-pattern guards

- Label clearly: UCF module is **supervised classification**, not unsupervised AD.
- Do not conflate crime classes with generic "anomaly score."

**Phase 7 implementation note:** SavedModels remain at the repository root (`Image Anomaly Detection-2/`, `Video Anomaly Detection/`). Configure paths via `configs/examples/vision.yaml`. Install optional `[vision]` extras for TensorFlow/OpenCV.

---

## Phase 8: Fairness & Bias Analysis (AIF360)

**Goal:** Measure whether detection disproportionately flags protected groups.

### 8.1 Fairness module

- Optional dep: `aif360`
- `src/anomaly_detection/fairness/metrics.py` — demographic parity, equalized odds
- `src/anomaly_detection/fairness/mitigation.py` — reweighing, threshold post-processing

### 8.2 Config

```yaml
fairness:
  protected_attributes: [gender, age_group]
  mitigation: reweighing   # or null
```

### 8.3 Dashboard data export

JSON report section: `fairness_metrics` appended to benchmark output.

### Verification checklist

- [ ] Fairness report generated on Adult/Credit dataset with synthetic groups
- [ ] Mitigation reduces disparity metric on test fixture
- [ ] Ethics disclaimer in `docs/ETHICS.md`

### Anti-pattern guards

- Require explicit `protected_attributes` in config; never auto-infer sensitive columns.

---

## Phase 9: Generative Models, LLMs & Multimodal

**Goal:** Advanced detection and natural-language explanations.

### 9.1 Diffusion / GAN-based detectors

- `models/generative/diffusion_detector.py` — reconstruction error scoring
- `models/generative/gan_augmentation.py` — synthetic rare anomalies for training
- Gate behind `extras` install: `pip install -e ".[generative]"`

### 9.2 LLM module

**Copy from:** PR branch `backend/app/llm/synthesizer.py` (Claude incident report pattern).

- `src/anomaly_detection/llm/explainer.py`:
  - Input: anomaly scores + feature context
  - Output: plain-language report (remediation steps)
- Prompt templates in `configs/prompts/anomaly_report.yaml`
- Support env var `ANTHROPIC_API_KEY` or OpenAI via LiteLLM

### 9.3 Multimodal fusion

- `src/anomaly_detection/multimodal/fusion.py` — shared latent space (multimodal autoencoder)
- Optional CLIP zero-shot path for image+text
- Document as experimental in README

### Verification checklist

- [ ] LLM explainer returns structured report given mock anomaly event
- [ ] Diffusion detector scores higher on injected image noise vs clean
- [ ] Multimodal fusion test on paired tabular+text fixture

### Anti-pattern guards

- LLM calls must be opt-in (`llm.enabled: false` default).
- Never send raw PII to LLM without redaction (reuse redaction patterns if ported from other projects).

---

## Phase 10: Governance, Tutorials & Performance Profiling

**Goal:** Community-ready project with domain tutorials and profiling.

### 10.1 Tutorials

Create `docs/tutorials/`:
- `01-tabular-fraud.md` + `configs/examples/fraud.yaml`
- `02-timeseries-iot.md`
- `03-vision-surveillance.md` (UCF)
- `04-streaming.md`
- `05-fairness.md`

### 10.2 Performance profiling

`src/anomaly_detection/evaluation/profiler.py`:
- Log wall time + peak memory per detector (inspired by dtaianomaly)
- Append to benchmark reports

### 10.3 Community

- GitHub issue templates: `bug_report.md`, `feature_request.md`
- Labels: `good first issue`, `phase-1`, … `phase-10`
- Public roadmap: link this file from README

### Verification checklist

- [ ] Each tutorial runs end-to-end with documented data
- [ ] Profiler output included in benchmark MD
- [ ] CONTRIBUTING.md references phase structure

---

## Phase 11: Final Verification & Release

### 11.1 Full test matrix

```bash
ruff check src tests
mypy src --ignore-missing-imports   # optional
pytest tests/ -v --cov=anomaly_detection
python -m anomaly_detection.cli.detect --config configs/default.yaml
python -m anomaly_detection.cli.benchmark --quick
```

### 11.2 Anti-pattern grep

```bash
# Should return zero in src/
git grep -E "submit\.php|require\('hhtp" -- src/
git grep -i "TBD" -- README.md      # replace all [TBD] placeholders
```

### 11.3 Documentation audit

- [ ] README matches implemented features per phase completed
- [ ] All registry datasets have license field
- [ ] API docs at `/docs` match actual routes
- [ ] CHANGELOG.md for v0.1.0 release

### 11.4 Release

- Tag `v0.1.0` after Phase 3 (minimal viable framework)
- Tag `v0.5.0` after Phase 7 (vision + tabular)
- Tag `v1.0.0` after Phase 11

---

## PR #1 Disposition Matrix

| PR #1 asset | Action |
|---|---|
| `backend/app/main.py` | Copy lifespan/CORS pattern → `src/anomaly_detection/api/app.py` |
| `backend/app/api/analyze.py` | Port to `/vision/*` in Phase 7 only |
| `backend/app/ml/model.py` | Refactor → `domains/vision/model_manager.py` |
| `backend/app/llm/synthesizer.py` | Copy → `llm/explainer.py` in Phase 9 |
| `frontend/` (Next.js) | Defer until Phase 9 dashboard; not blocking framework |
| `.github/workflows/ci.yml` | Simplify and adopt in Phase 1 |
| `docker-compose.yml` | Adopt in Phase 3 with tabular API only |

**Recommendation:** Close PR #1 after extracting patterns; open new PRs per phase.

---

## Execution Order Summary

| Phase | Scope | Est. effort | Depends on |
|---|---|---|---|
| 0 | Discovery | Done | — |
| 1 | Foundation & CI | 2–3 days | 0 |
| 2 | Detectors + config | 3–5 days | 1 |
| 3 | CLI + REST API | 2–3 days | 2 |
| 4 | Dataset registry + benchmarks | 3–4 days | 2 |
| 5 | Streaming (PySAD) | 3–4 days | 2 |
| 6 | RCA (PyRCA) | 4–5 days | 3 |
| 7 | Vision domain (existing work) | 3–4 days | 1 |
| 8 | Fairness (AIF360) | 3–4 days | 4 |
| 9 | Generative + LLM + multimodal | 1–2 weeks | 3, 7 |
| 10 | Tutorials + governance | 3–5 days | 3+ |
| 11 | Final verification + release | 2 days | All |

**Start immediately with Phase 1** in a new chat:

> "Execute Phase 1 of `docs/EXECUTION_PLAN.md` for anomaly-detection repo at `/Users/abhinaysaikamineni/gh-cleanup/anomaly-detection`."

---

## References

- Repository: https://github.com/askmy-stack/anomaly-detection
- Open PR #1: https://github.com/askmy-stack/anomaly-detection/pull/1
- scikit-learn outlier detection: https://scikit-learn.org/stable/modules/outlier_detection.html
- PyOD: https://pyod.readthedocs.io/
- dtaianomaly: https://dtaianomaly.readthedocs.io/
- Orion: https://orion.readthedocs.io/
- PySAD: https://pysad.readthedocs.io/
- PyRCA: https://pyrca.readthedocs.io/
- AIF360: https://aif360.readthedocs.io/
