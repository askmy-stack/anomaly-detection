#!/usr/bin/env python3
"""Generate the Py-outlier demo GIF for the README."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "assets" / "py-outlier-demo.gif"
TITLE = "Py-outlier — anomaly detection demo"

# Dark theme palette
BG = "#0d1117"
FG = "#e6edf3"
NORMAL = "#58a6ff"
OUTLIER = "#f0883e"
BOUNDARY = "#8b949e"


def _make_data(seed: int = 42) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    n_normal = 120
    n_outliers = 8

    normal = rng.normal(loc=(0.0, 0.0), scale=0.55, size=(n_normal, 2))
    outliers = rng.uniform(low=-2.8, high=2.8, size=(n_outliers, 2))
    # Push outliers away from dense cluster
    dist = np.linalg.norm(outliers, axis=1)
    mask = dist < 1.4
    outliers[mask] *= 1.8

    points = np.vstack([normal, outliers])
    labels = np.array([0] * n_normal + [1] * n_outliers)
    return points, labels


def generate(output: Path = OUTPUT, frames: int = 48) -> Path:
    output.parent.mkdir(parents=True, exist_ok=True)
    points, labels = _make_data()

    fig, ax = plt.subplots(figsize=(6.4, 4.8), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_title(TITLE, color=FG, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(-3.2, 3.2)
    ax.set_aspect("equal")
    ax.tick_params(colors=FG, labelsize=9)
    for spine in ax.spines.values():
        spine.set_color("#30363d")

    normal_pts = points[labels == 0]
    outlier_pts = points[labels == 1]

    ax.scatter(
        normal_pts[:, 0],
        normal_pts[:, 1],
        c=NORMAL,
        s=36,
        alpha=0.85,
        edgecolors="none",
        zorder=2,
    )
    scatter_outliers = ax.scatter(
        outlier_pts[:, 0],
        outlier_pts[:, 1],
        facecolors="none",
        edgecolors=OUTLIER,
        s=220,
        linewidths=2.2,
        zorder=4,
    )

    theta = np.linspace(0, 2 * np.pi, 200)
    radius = 1.35
    boundary, = ax.plot([], [], color=BOUNDARY, linestyle="--", linewidth=1.4, zorder=1)
    ax.text(
        0.02,
        0.02,
        "normal cluster",
        transform=ax.transAxes,
        color=NORMAL,
        fontsize=9,
        alpha=0.9,
    )
    ax.text(
        0.02,
        0.08,
        "flagged outliers",
        transform=ax.transAxes,
        color=OUTLIER,
        fontsize=9,
        alpha=0.9,
    )

    def update(frame: int):
        pulse = 0.92 + 0.08 * np.sin(2 * np.pi * frame / frames)
        scatter_outliers.set_sizes(np.full(len(outlier_pts), 220 * pulse))
        boundary.set_data(radius * pulse * np.cos(theta), radius * pulse * np.sin(theta))
        return scatter_outliers, boundary

    anim = FuncAnimation(fig, update, frames=frames, interval=70, blit=True)
    writer = PillowWriter(fps=12)
    anim.save(output, writer=writer, dpi=100)
    plt.close(fig)
    return output


if __name__ == "__main__":
    path = generate()
    print(f"Wrote {path}")
