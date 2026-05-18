"""Prediction request and response schemas."""

from typing import Literal

from pydantic import BaseModel, Field, field_validator

SupportCategory = Literal[
    "ORDER",
    "SHIPPING",
    "CANCEL",
    "INVOICE",
    "PAYMENT",
    "REFUND",
    "FEEDBACK",
    "CONTACT",
    "ACCOUNT",
    "DELIVERY",
    "SUBSCRIPTION",
]

SUPPORT_CATEGORIES: tuple[str, ...] = (
    "ORDER",
    "SHIPPING",
    "CANCEL",
    "INVOICE",
    "PAYMENT",
    "REFUND",
    "FEEDBACK",
    "CONTACT",
    "ACCOUNT",
    "DELIVERY",
    "SUBSCRIPTION",
)


class PredictionInput(BaseModel):
    """Input payload for customer support category prediction."""

    instruction: str = Field(
        min_length=1,
        max_length=5000,
        description="Customer support request text.",
        examples=["I need to track my order"],
    )

    @field_validator("instruction")
    @classmethod
    def validate_instruction(cls, value: str) -> str:
        """Normalize and validate the request text."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("La solicitud no puede estar vacia.")
        return normalized


class PredictionOutput(BaseModel):
    """Prediction response returned to API clients."""

    prediction: SupportCategory
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    model_version: str
    pipeline_version: str
