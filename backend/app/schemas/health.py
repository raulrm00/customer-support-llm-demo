"""Health response schemas."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health endpoint response."""

    status: str
    service: str
    version: str
