from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

settings = get_settings()


def _create_engine_from_url(url: str):
    """Create SQLAlchemy engine with sensible defaults for SQLite testing.

    - For SQLite file-based DBs, enable check_same_thread=False.
    - For SQLite in-memory ("sqlite://" or "sqlite:///:memory:"), use StaticPool
      so the memory database persists across connections.
    """
    url_str = str(url)
    if url_str.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
        if url_str in ("sqlite://", "sqlite:///:memory:"):
            return create_engine(
                url_str, connect_args=connect_args, poolclass=StaticPool
            )
        return create_engine(url_str, connect_args=connect_args)
    return create_engine(url_str)


engine = _create_engine_from_url(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
