from typing import Any
from fastapi.responses import JSONResponse

from app.schemas.success import SuccessResponse

def success_response(
    *,
    data: Any,
    message: str,
    status_code: int = 200,
):
    payload = SuccessResponse(
        data=data,
        message=message,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(),
    )
