"""Prediction routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api import deps
from app.core.config import Settings, get_settings
from app.models.user import User
from app.schemas.prediction import PredictionInput, PredictionOutput
from app.services.model_loader import load_model_bundle
from app.services.prediction_service import PredictionService

router = APIRouter()


def get_prediction_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> PredictionService:
    """Build the prediction service for request handling."""
    bundle = load_model_bundle(settings)
    return PredictionService(bundle=bundle)


@router.post(
    "/predictions",
    response_model=PredictionOutput,
    status_code=status.HTTP_200_OK,
    summary="Classify a support request",
    description="Predicts the customer support category for an incoming request.",
)
def predict_category(
    payload: PredictionInput,
    service: Annotated[PredictionService, Depends(get_prediction_service)],
    _user: Annotated[User, Depends(deps.check_usage_limit)],
) -> PredictionOutput:
    """Predict the support category for a single incoming request."""
    return service.predict(payload)
