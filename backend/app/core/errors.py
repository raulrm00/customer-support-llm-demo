"""Application exception handling."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.services.model_loader import ModelNotLoadedError


def register_exception_handlers(app: FastAPI) -> None:
    """Register safe API exception handlers."""

    @app.exception_handler(ModelNotLoadedError)
    async def model_not_loaded_handler(
        _request: Request,
        exc: ModelNotLoadedError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "detail": "El modelo de predicción no está disponible.",
                "error_code": exc.error_code,
            },
        )
