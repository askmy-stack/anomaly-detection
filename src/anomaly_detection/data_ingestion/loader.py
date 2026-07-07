"""CSV data loading utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def load_csv(
    path: str | Path,
    target_column: str | None = None,
) -> tuple[np.ndarray, np.ndarray | None, list[str]]:
    """Load feature matrix and optional labels from a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Dataset not found: {csv_path}")

    frame = pd.read_csv(csv_path)
    if frame.empty:
        raise ValueError(f"Dataset is empty: {csv_path}")

    labels: np.ndarray | None = None
    feature_frame = frame
    if target_column:
        if target_column not in frame.columns:
            raise ValueError(f"Target column '{target_column}' not found in {csv_path}")
        labels = frame[target_column].to_numpy()
        feature_frame = frame.drop(columns=[target_column])

    feature_names = list(feature_frame.columns)
    features = feature_frame.to_numpy(dtype=float)
    return features, labels, feature_names
