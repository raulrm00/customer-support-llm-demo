"""Train and persist the customer support text classifier."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import joblib
import yaml
from dvclive import Live  # type: ignore[attr-defined]
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.evaluation.metrics import classification_metrics
from src.preprocessing.cleaning import load_dataset
from src.schemas.customer_support import ProcessedCustomerSupportSchema


def load_params(path: Path) -> dict[str, Any]:
    """Load training parameters from YAML."""
    with path.open(encoding="utf-8") as file:
        params = yaml.safe_load(file) or {}
    if not isinstance(params, dict):
        raise ValueError("params.yaml must contain a mapping.")
    return params


def build_pipeline(
    stop_words: str | None, max_iter: int, random_state: int
) -> Pipeline:
    """Build the full preprocessing and classification pipeline."""
    preprocessor = ColumnTransformer(
        transformers=[
            ("tfidf", TfidfVectorizer(stop_words=stop_words), "instruction"),
        ],
        remainder="drop",
    )
    return Pipeline(
        steps=[
            ("preprocess", preprocessor),
            (
                "classifier",
                LogisticRegression(max_iter=max_iter, random_state=random_state),
            ),
        ]
    )


def log_experiment(
    project_dir: Path,
    training_params: dict[str, Any],
    metrics: dict[str, float],
) -> None:
    """Log metrics with DVCLive when DVC is initialized."""
    live_dir = project_dir / "dvclive"
    live_dir.mkdir(parents=True, exist_ok=True)

    if (project_dir / ".dvc").exists():
        with Live(
            dir=str(live_dir),
            save_dvc_exp=False,
            dvcyaml=False,
        ) as live:
            live.log_params(training_params)
            for name, value in metrics.items():
                live.log_metric(name, value)
        return

    with (live_dir / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, sort_keys=True)
    with (live_dir / "params.json").open("w", encoding="utf-8") as file:
        json.dump(training_params, file, indent=2, sort_keys=True)


def train_model(params: dict[str, Any], project_dir: Path) -> dict[str, float]:
    """Train, evaluate, and persist the model pipeline."""
    data_params = params["data"]
    training_params = params["training"]
    artifact_params = params["artifacts"]

    input_path = (project_dir / data_params["input_path"]).resolve()
    model_path = project_dir / artifact_params["model_path"]
    metadata_path = project_dir / artifact_params["metadata_path"]
    model_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe = load_dataset(input_path)
    validated = ProcessedCustomerSupportSchema.validate(dataframe)

    text_column = str(data_params["text_column"])
    target_column = str(data_params["target_column"])
    features = validated[[text_column]]
    target = validated[target_column]

    random_state = int(training_params["random_state"])
    test_size = float(training_params["test_size"])
    validation_size = float(training_params["validation_size"])

    x_train_validation, x_test, y_train_validation, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )
    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_validation,
        y_train_validation,
        test_size=validation_size,
        random_state=random_state,
        stratify=y_train_validation,
    )

    pipeline = build_pipeline(
        stop_words=(
            str(training_params["stop_words"])
            if training_params.get("stop_words")
            else None
        ),
        max_iter=int(training_params["max_iter"]),
        random_state=random_state,
    )
    pipeline.fit(x_train, y_train)

    metrics = {
        **classification_metrics(y_train, pipeline.predict(x_train), "train"),
        **classification_metrics(
            y_validation, pipeline.predict(x_validation), "validation"
        ),
        **classification_metrics(y_test, pipeline.predict(x_test), "test"),
    }

    joblib.dump(pipeline, model_path)
    metadata = {
        "model_version": "1.0.0",
        "pipeline_version": "1.0.0",
        "artifact_name": model_path.name,
        "created_at": datetime.now(UTC).isoformat(),
        "input_schema": {"required_columns": [text_column]},
        "target_column": target_column,
        "training_rows": int(len(x_train)),
        "validation_rows": int(len(x_validation)),
        "test_rows": int(len(x_test)),
        "metrics": metrics,
    }
    with metadata_path.open("w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, sort_keys=True)

    log_experiment(project_dir, training_params, metrics)
    return metrics


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--params",
        type=Path,
        default=Path("params.yaml"),
        help="Path to params.yaml relative to the ml directory.",
    )
    return parser.parse_args()


def main() -> None:
    """Train the model from the command line."""
    args = parse_args()
    project_dir = Path.cwd()
    params = load_params(project_dir / args.params)
    metrics = train_model(params=params, project_dir=project_dir)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
