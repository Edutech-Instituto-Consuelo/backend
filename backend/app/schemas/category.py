from pydantic import BaseModel, Field
from typing import Annotated, Optional

nameType = Annotated[str,Field(min_length=1,max_length=100, description="nome da categoria")]
descriptionType = Annotated[str, Field(min_length=1, max_length=500, description="descroção da categoria")]


class CategoriaBase(BaseModel):
	"""Schema base da categoria"""
	nome: nameType
	descricao: descriptionType

class CategoriaCreate(CategoriaBase):
	"""Schema de criação da categoria"""
	pass

class CategoriaResponse(CategoriaBase):
	"""Schema de resposta da categoria"""
	id = int

	class Config:
		from_attributes = True

class CategoriaUpdate(BaseModel):
	"""Schema de update , metodo patch"""

	name: Optional[nameType] = None
	descricao: Optional[descriptionType] = None


