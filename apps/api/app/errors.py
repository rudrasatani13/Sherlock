from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .config import get_settings
from .logging import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: Optional[Any] = None) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class NotImplementedApiError(AppError):
    def __init__(self, module: str, details: Optional[Any] = None) -> None:
        super().__init__(
            status_code=501,
            code="not_implemented",
            message=f"The {module} API is a Phase 9 placeholder and is not implemented yet.",
            details=details,
        )


def build_metadata() -> Dict[str, str]:
    settings = get_settings()
    return {
        "api_version": settings.api_version,
        "phase": settings.current_phase,
        "environment": settings.environment,
    }


def build_error_response(code: str, message: str, details: Optional[Any] = None) -> Dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "metadata": build_metadata(),
    }


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, error: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=error.status_code,
            content=build_error_response(error.code, error.message, error.details),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=build_error_response("validation_error", "Request validation failed.", error.errors()),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, error: StarletteHTTPException) -> JSONResponse:
        if error.status_code == 404:
            return JSONResponse(
                status_code=404,
                content=build_error_response("not_found", "The requested API route was not found."),
            )
        return JSONResponse(
            status_code=error.status_code,
            content=build_error_response("http_error", str(error.detail)),
        )

    @app.exception_handler(Exception)
    async def internal_error_handler(request: Request, error: Exception) -> JSONResponse:
        logger.exception("Unhandled API error")
        return JSONResponse(
            status_code=500,
            content=build_error_response("internal_error", "An unexpected internal error occurred."),
        )
