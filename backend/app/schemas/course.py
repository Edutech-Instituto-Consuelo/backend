from pydantic import BaseModel, Field
from typing import Annotated, Optional
from datetime import datetime

tituloType = Annotated[str, Field(max_length=200, min_length=1, description="Titulo do curso")]
descricaoType = Annotated[str, Field(max_length=500, min_length=1, description="Descrição do curso")]
cargaHorariaType = Annotated[int, Field(gt=0, description="Carga Horaria do curso")]
idInstrutorType = Annotated[int, Field(gt=0, description="Id do instrutor")]
idNivelType = Annotated[int, Field(gt=0, description="Id do nivel")]
idCategoria = Annotated[int, Field(gt=0, description="Id da Categoria")]
InstrutorOrNivel = Annotated[str, Field(max_length=200, description="Nome do instrutor ou Nivel")]
mediaAvaliacao = Annotated[float, Field(default=0.0, description="Media de avalições")]
qtdAvaliacao = Annotated[int, Field(default=0, description="quantidade de avaliações")]
precoType = Annotated[float, Field(default=0.0, description="Preço do curso")]
urlImageType = Annotated[str, Field(max_length=255, description="URL da imagem do curso")
]
class CursoResponse(BaseModel):
	id: int
	url_image : Optional[urlImageType] = None
	titulo: tituloType
	id_instrutor: int
	instrutor: InstrutorOrNivel
	id_nivel: int
	nivel: InstrutorOrNivel
	avaliacao: mediaAvaliacao
	quantidade_avaliacoes: qtdAvaliacao
	preco: precoType

	class Config:
		from_attributes = True

class CursoEspecificoResponse(BaseModel):
	id: int
	titulo: tituloType
	descricao: descricaoType
	avaliacao: mediaAvaliacao
	quantidade_avaliacoes: qtdAvaliacao
	quantidade_horas: int
	id_nivel: int
	nivel: InstrutorOrNivel
	preco: precoType
	id_instrutor: int
	instrutor: InstrutorOrNivel
	id_especialidade: int
	especialidade_instrutor: str

	class Config:
		from_attributes = True
