"""Tests for the DVC training configuration."""

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping from disk."""
    with path.open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    assert isinstance(data, dict)
    return data


def test_training_data_path_uses_ml_data_directory() -> None:
    """The default training dataset must not be read from refs."""
    params = load_yaml(Path("params.yaml"))

    input_path = Path(params["data"]["input_path"])

    assert input_path.parts[:2] == ("data", "raw")
    assert "refs" not in input_path.parts


def test_dvc_train_stage_uses_versioned_ml_dataset() -> None:
    """The DVC pipeline must depend on the copied ML dataset."""
    dvc_config = load_yaml(Path("dvc.yaml"))

    deps = dvc_config["stages"]["train"]["deps"]

    assert "data/raw/bitext-limpio.parquet" in deps
    assert all("refs" not in Path(dep).parts for dep in deps)
