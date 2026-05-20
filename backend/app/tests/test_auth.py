import os

os.environ.setdefault("DATABASE_URL", "sqlite://")


import pytest
from fastapi.testclient import TestClient

from app.core import security
from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.user import User


@pytest.fixture(autouse=True)
def setup_db():
    """Create DB tables and a test user for each test run."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Create a test user
    user = User(
        email="test@example.com",
        password_hash=security.get_password_hash("password123"),
        is_active=True,
        daily_limit_seconds=10.0,
    )
    db.add(user)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_login_success():
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid_password():
    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_protected_access_without_token():
    client = TestClient(app)
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_protected_access_with_invalid_token():
    client = TestClient(app)
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
