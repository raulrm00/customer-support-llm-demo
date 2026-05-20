"""Domain model package reserved for future backend models."""

from app.db.session import Base
from app.models.user import User

__all__ = ["Base", "User"]
