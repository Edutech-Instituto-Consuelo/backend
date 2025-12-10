from pydantic import BaseModel, Field
from typing import Annotated, Optional


descriptionType = Annotated[str, Field(min_length=1, max_length=20, description="descrição do nivel")]


class NivelBase(BaseModel):
	"""Schema base da nivel"""
	descricao: descriptionType

class NivelCreate(NivelBase):
	"""Schema de criação da nivel"""
	pass

class NivelResponse(NivelBase):
	"""Schema de resposta da nivel"""
	id: int

	class Config:
		from_attributes = True

class NivelUpdate(BaseModel):
	"""Schema de update , metodo patch"""

	descricao: Optional[descriptionType] = None

