"""API v1 route registration."""

from fastapi import APIRouter

from app.api.v1 import health, predictions

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(predictions.router, tags=["predictions"])
