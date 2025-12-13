from typing import Any
from pydantic import BaseModel, Field

class SuccessResponse(BaseModel):
    data: Any
    message: str = Field(..., examples=["Operação realizada com sucesso."])
