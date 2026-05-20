"""Tests for prediction endpoint behavior."""

import os

os.environ.setdefault("DATABASE_URL", "sqlite://")

from fastapi.testclient import TestClient

from app.api import deps
from app.api.v1.predictions import get_prediction_service
from app.main import app
from app.models.user import User
from app.services.model_loader import ModelBundle
from app.services.prediction_service import PredictionService


class FakePipeline:
    """Small fake pipeline used to avoid loading a real model artifact."""

    def predict(self, features: object) -> list[str]:
        return ["ORDER"]

    def predict_proba(self, features: object) -> list[list[float]]:
        return [[0.92, 0.08]]


def override_prediction_service() -> PredictionService:
    """Return a prediction service backed by a fake pipeline."""
    return PredictionService(
        bundle=ModelBundle(
            pipeline=FakePipeline(),
            model_version="test-model",
            pipeline_version="test-pipeline",
        )
    )


def override_check_usage_limit() -> User:
    """Mock usage limit check for testing."""
    return User(
        email="test@example.com",
        is_active=True,
        daily_limit_seconds=100.0,
        daily_usage_seconds=0.0,
    )


def test_prediction_endpoint_returns_category_and_metadata() -> None:
    """Prediction endpoint returns the model output contract."""
    app.dependency_overrides[get_prediction_service] = override_prediction_service
    app.dependency_overrides[deps.check_usage_limit] = override_check_usage_limit
    client = TestClient(app)

    response = client.post(
        "/api/v1/predictions",
        json={"instruction": "Where is my order?"},
    )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json() == {
        "prediction": "ORDER",
        "confidence": 0.92,
        "model_version": "test-model",
        "pipeline_version": "test-pipeline",
    }


def test_prediction_endpoint_rejects_blank_instruction() -> None:
    """Prediction endpoint validates required request text."""
    app.dependency_overrides[get_prediction_service] = override_prediction_service
    app.dependency_overrides[deps.check_usage_limit] = override_check_usage_limit
    client = TestClient(app)

    response = client.post("/api/v1/predictions", json={"instruction": ""})

    app.dependency_overrides.clear()

    assert response.status_code == 422
