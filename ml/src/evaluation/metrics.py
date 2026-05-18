"""Evaluation metrics for classifier training."""

from typing import Any

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def classification_metrics(y_true: Any, y_pred: Any, prefix: str) -> dict[str, float]:
    """Calculate weighted classification metrics."""
    return {
        f"{prefix}_accuracy": float(accuracy_score(y_true, y_pred)),
        f"{prefix}_precision_weighted": float(
            precision_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
        f"{prefix}_recall_weighted": float(
            recall_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
        f"{prefix}_f1_weighted": float(
            f1_score(y_true, y_pred, average="weighted", zero_division=0)
        ),
    }
