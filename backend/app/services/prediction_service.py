"""Prediction service layer."""

from typing import Any, cast

import pandas as pd

from app.schemas.prediction import (
    SUPPORT_CATEGORIES,
    PredictionInput,
    PredictionOutput,
    SupportCategory,
)
from app.services.model_loader import ModelBundle


class PredictionService:
    """Generate category predictions using the loaded model pipeline."""

    def __init__(self, bundle: ModelBundle) -> None:
        self._bundle = bundle

    def predict(self, payload: PredictionInput) -> PredictionOutput:
        """Predict a support category from validated input."""
        features = pd.DataFrame([{"instruction": payload.instruction}])
        raw_prediction = str(self._bundle.pipeline.predict(features)[0])
        if raw_prediction not in SUPPORT_CATEGORIES:
            raise ValueError("The model returned an unsupported category.")
        confidence = self._predict_confidence(features)

        return PredictionOutput(
            prediction=cast(SupportCategory, raw_prediction),
            confidence=confidence,
            model_version=self._bundle.model_version,
            pipeline_version=self._bundle.pipeline_version,
        )

    def _predict_confidence(self, features: pd.DataFrame) -> float | None:
        predict_proba = getattr(self._bundle.pipeline, "predict_proba", None)
        if not callable(predict_proba):
            return None
        probabilities: Any = predict_proba(features)
        if len(probabilities) == 0:
            return None
        return float(max(probabilities[0]))
