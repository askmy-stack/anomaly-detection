"""Pydantic schemas for the REST API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = "ok"


class ModelsResponse(BaseModel):
    models: list[str]


class DetectRequest(BaseModel):
    data: list[list[float]] = Field(..., min_length=1)
    config: dict[str, Any] | None = None


class DetectResponse(BaseModel):
    model: str | None
    n_samples: int
    n_anomalies: int
    scores: list[float]
    predictions: list[int]
    metrics: dict[str, float] | None = None


class BatchDetectResponse(DetectResponse):
    feature_names: list[str] = Field(default_factory=list)
