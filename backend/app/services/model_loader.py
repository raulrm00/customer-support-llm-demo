"""Model artifact loading utilities."""

import json
from dataclasses import dataclass
from functools import lru_cache
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import joblib

from app.core.config import Settings


class ModelNotLoadedError(RuntimeError):
    """Raised when the prediction pipeline cannot be loaded."""

    error_code = "MODEL_NOT_LOADED"


@dataclass(frozen=True)
class ModelBundle:
    """Loaded model pipeline and associated metadata."""

    pipeline: Any
    model_version: str
    pipeline_version: str


def resolve_project_path(path: Path) -> Path:
    """Resolve paths relative to the repository root."""
    if path.is_absolute():
        return path
    repository_root = Path(__file__).resolve().parents[3]
    return repository_root / path


def load_model_bundle(settings: Settings) -> ModelBundle:
    """Load the configured model pipeline and metadata."""
    return _load_model_bundle(
        str(settings.model_artifact_path),
        str(settings.model_metadata_path) if settings.model_metadata_path else "",
        settings.model_version,
        settings.pipeline_version,
    )


@lru_cache
def _load_model_bundle(
    artifact_path: str,
    metadata_path: str,
    default_model_version: str,
    default_pipeline_version: str,
) -> ModelBundle:
    resolved_artifact_path = resolve_project_path(Path(artifact_path))
    if not resolved_artifact_path.exists():
        raise ModelNotLoadedError(
            f"Model artifact not found at {resolved_artifact_path}"
        )

    pipeline = joblib.load(resolved_artifact_path)
    if not hasattr(pipeline, "predict"):
        raise ModelNotLoadedError("Loaded artifact does not expose predict().")

    metadata = _load_metadata(Path(metadata_path)) if metadata_path else {}
    return ModelBundle(
        pipeline=pipeline,
        model_version=str(metadata.get("model_version", default_model_version)),
        pipeline_version=str(
            metadata.get("pipeline_version", default_pipeline_version)
        ),
    )


def _load_metadata(path: Path) -> dict[str, Any]:
    resolved_metadata_path = resolve_project_path(path)
    if not resolved_metadata_path.exists():
        return {}
    try:
        with resolved_metadata_path.open(encoding="utf-8") as file:
            metadata = json.load(file)
    except (OSError, JSONDecodeError) as exc:
        raise ModelNotLoadedError("Model metadata could not be read.") from exc
    if not isinstance(metadata, dict):
        raise ModelNotLoadedError("Model metadata must be a JSON object.")
    return metadata
