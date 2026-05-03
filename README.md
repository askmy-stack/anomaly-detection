# anomaly-detection

> Anomaly detection on structured datasets using statistical and machine learning methods.

Implements and compares anomaly detection techniques — from statistical baselines (z-score, IQR) to ML approaches (Isolation Forest, Autoencoder).

## What it does

- Ingests structured time-series or tabular data
- Applies statistical anomaly detection (z-score, IQR bounds)
- Trains ML-based detectors (Isolation Forest, One-Class SVM, Autoencoder)
- Evaluates precision/recall on labeled anomaly sets
- Visualizes detected anomalies with confidence scores

## Stack

- **Languages:** Python
- **ML:** scikit-learn, PyTorch
- **Tooling:** Jupyter Notebook, matplotlib

## Results

| Metric | Value |
|---|---|
| Methods compared | [TBD] |
| Best F1 | [TBD] |
| Dataset | [TBD] |

## Setup

```bash
git clone https://github.com/askmy-stack/anomaly-detection.git
cd anomaly-detection
pip install -r requirements.txt
jupyter notebook
```

## License

MIT

---

Built by [Abhinaysai Kamineni](https://github.com/askmy-stack)
