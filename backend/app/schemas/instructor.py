from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

biografiaType = Annotated[str, Field(max_length=300, description="Biografia do instrutor")]

class InstrutorEspecificoResponse(BaseModel):
	id:int
	nome: str
	id_especialidade: int
	especialidade: str
	biografia: biografiaType

	class Config:
		from_attributes = True
