from typing import Optional, Annotated
from pydantic import BaseModel, Field


DescricaoType = Annotated[str, Field(min_length=1, max_length=200, description="")]

# Base
class StatusCursoBase(BaseModel):
    descricao: DescricaoType


# Usado para atualizar um status com PUT
class StatusCursoUpdate(StatusCursoBase):
    descricao: DescricaoType


# Schema de saída 
class StatusCursoResponse(BaseModel):
  
    id: int
    descricao: DescricaoType

    class Config:
        orm_mode = True


# Usado para criar um novo status
class StatusCursoCriar(StatusCursoBase):
    pass

# Usado para apagar um status 
class StatusCursoDeletar(StatusCursoBase):
    pass