import time
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/access-token")


def get_current_user(
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str, Depends(reusable_oauth2)],
) -> User:
    """Validate JWT and return current user."""
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def check_usage_limit(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Generator[User]:
    """
    Check and update daily API usage limit.
    Handles automatic reset every 24 hours.
    """
    now = datetime.now(UTC)

    # 1. Automatic Reset every 24h
    # Ensure both datetimes are timezone-aware (SQLite may return naive datetimes)
    reset_at = current_user.daily_usage_reset_at
    if reset_at is None:
        # If missing, initialize to now
        reset_at = now
    if reset_at.tzinfo is None:
        # Treat naive timestamps as UTC
        reset_at = reset_at.replace(tzinfo=UTC)

    time_since_reset = now - reset_at
    if time_since_reset.total_seconds() >= 86400:
        current_user.daily_usage_seconds = 0.0
        current_user.daily_usage_reset_at = now
        db.add(current_user)
        db.commit()
        db.refresh(current_user)

    # 2. Check if limit exceeded
    if current_user.daily_usage_seconds >= current_user.daily_limit_seconds:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Daily API usage limit exceeded",
        )

    # 3. Measure time
    start_time = time.time()

    yield current_user

    # 4. Update usage after request
    duration = time.time() - start_time
    current_user.daily_usage_seconds += duration
    db.add(current_user)
    db.commit()
