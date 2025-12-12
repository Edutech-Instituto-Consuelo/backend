from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.error import ErrorResponse
from app.core.exceptions import AppException

async def app_exception_handler(request: Request, exc: AppException):
    payload = ErrorResponse(
        data=exc.data,
        message=exc.message,
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    payload = ErrorResponse(
        data=exc.errors(),
        message="Erro de validação na requisição.",
    )
    return JSONResponse(status_code=422, content=payload.model_dump())

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    payload = ErrorResponse(
        data=None,
        message=str(exc.detail) if exc.detail else "Erro na requisição.",
    )
    return JSONResponse(status_code=exc.status_code, content=payload.model_dump())

async def unhandled_exception_handler(request: Request, exc: Exception):
    payload = ErrorResponse(
        data=None,
        message="Erro interno inesperado.",
    )
    return JSONResponse(status_code=500, content=payload.model_dump())
