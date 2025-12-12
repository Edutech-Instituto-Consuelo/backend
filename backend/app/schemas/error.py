from typing import Any
from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    data: Any = None
    message: str = Field(..., examples=["Erro ao processar a requisição."])
