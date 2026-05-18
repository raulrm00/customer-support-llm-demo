"""Tests for health endpoint behavior."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_expected_shape() -> None:
    """Health endpoint returns a safe process status response."""
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "backend",
        "version": "1.0.0",
    }
