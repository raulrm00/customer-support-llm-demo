import json
import shutil
from pathlib import Path

import joblib
import pytest

from app.services.model_loader import ModelNotLoadedError, _load_model_bundle

TEST_DIR = Path(__file__).resolve().parent / "tmp_model_loader"


class _DummyPipelineWithProba:
    def predict(self, X):
        return ["ORDER"]

    def predict_proba(self, X):
        return [[0.6, 0.4]]


class _DummyPipeline:
    def predict(self, X):
        return ["ORDER"]


def _ensure_test_dir() -> Path:
    TEST_DIR.mkdir(exist_ok=True)
    return TEST_DIR


def _cleanup_test_dir() -> None:
    if TEST_DIR.exists():
        shutil.rmtree(TEST_DIR)


def test_missing_artifact_raises() -> None:
    _load_model_bundle.cache_clear()
    with pytest.raises(ModelNotLoadedError):
        _load_model_bundle("nonexistent_artifact.joblib", "", "dmodel", "dpipeline")


def test_load_bundle_with_valid_artifact_and_metadata() -> None:
    _load_model_bundle.cache_clear()
    tmp = _ensure_test_dir()

    artifact = tmp / "pipeline.joblib"
    joblib.dump(_DummyPipelineWithProba(), str(artifact))

    metadata = tmp / "metadata.json"
    metadata.write_text(
        json.dumps({"model_version": "m-test", "pipeline_version": "p-test"})
    )

    bundle = _load_model_bundle(str(artifact), str(metadata), "default-m", "default-p")
    assert hasattr(bundle.pipeline, "predict")
    assert bundle.model_version == "m-test"
    assert bundle.pipeline_version == "p-test"

    _load_model_bundle.cache_clear()
    _cleanup_test_dir()


def test_invalid_metadata_raises() -> None:
    _load_model_bundle.cache_clear()
    tmp = _ensure_test_dir()

    artifact = tmp / "pipeline.joblib"
    joblib.dump(_DummyPipeline(), str(artifact))

    metadata = tmp / "metadata.json"
    # Write invalid JSON (a JSON string instead of object)
    metadata.write_text(json.dumps("not-an-object"))

    with pytest.raises(ModelNotLoadedError):
        _load_model_bundle(str(artifact), str(metadata), "default-m", "default-p")

    _load_model_bundle.cache_clear()
    _cleanup_test_dir()
