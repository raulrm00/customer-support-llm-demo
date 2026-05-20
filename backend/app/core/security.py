import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import jwt

from app.core.config import get_settings

settings = get_settings()


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    """Generate a JWT access token."""
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.jwt_access_token_expire_minutes
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def _sha256_bytes(password: str) -> bytes:
    """Return SHA-256 digest of the UTF-8 encoded password as bytes."""
    return hashlib.sha256(password.encode("utf-8")).digest()


def get_password_hash(password: str) -> str:
    """Generate a hash for a plain text password.

    This uses a SHA-256 pre-hash to avoid bcrypt's 72-byte limitation and stores
    the resulting bcrypt hash as a UTF-8 string.
    """
    hashed = bcrypt.hashpw(_sha256_bytes(password), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against its hash.

    Applies the same SHA-256 pre-hash before verifying with bcrypt.
    """
    try:
        return bcrypt.checkpw(
            _sha256_bytes(plain_password), hashed_password.encode("utf-8")
        )
    except Exception:
        return False
