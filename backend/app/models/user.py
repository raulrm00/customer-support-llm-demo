
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.db.session import Base


class User(Base):
    """User model for authentication and usage tracking."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Daily usage limits
    daily_usage_seconds = Column(Float, default=0.0)
    daily_usage_reset_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    daily_limit_seconds = Column(Float, nullable=False)
