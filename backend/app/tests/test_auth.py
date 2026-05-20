import time
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import Base, get_db
from app.core import security
from app.models.user import User

# Setup in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Create a test user
    user = User(
        email="test@example.com",
        password_hash=security.get_password_hash("password123"),
        is_active=True,
        daily_limit_seconds=10.0,
    )
    db.add(user)
    db.commit()
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
