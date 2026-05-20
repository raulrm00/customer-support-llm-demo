"""Application configuration."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    app_env: str = "local"
    app_name: str = "Customer Support Classifier API"
    api_version: str = "1.0.0"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:4200"]
    )
    model_artifact_path: Path = Path("ml/models/modelo_idf.joblib")
    model_metadata_path: Path | None = Path("ml/models/model_metadata.json")
    model_version: str = "1.0.0"
    pipeline_version: str = "1.0.0"
    log_level: str = "INFO"

    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/customer_support"

    # Auth
    jwt_secret_key: str = "yoursecretkeyhere"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    # Usage Limits
    default_daily_limit_seconds: int = 3600

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        """Parse comma-separated CORS origins from environment variables."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
