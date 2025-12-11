from pydantic import BaseModel, Field
from typing import Optional, Annotated
from datetime import datetime

# Tipos anotados com validações
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
urlImageType = Annotated[str, Field(max_length=255, description="URL da imagem do curso")]

# Tipos anotados para controle
SobreType = Annotated[str, Field(min_length=1, description="Texto sobre o curso")]
IdCategoriaType = Annotated[int, Field(gt=0, description="Id da categoria")]
PrecoOptionalType = Annotated[
    Optional[float],
    Field(ge=0, description="Preço do curso (pode ser nulo, default 0)")
]

##===================== CURSO (BASE) ========================##
# Respostas públicas (sem dados sensíveis)
class CursoBase(BaseModel):
    id: int
    # url_image: Optional[urlImageType] = None
    titulo: tituloType
    id_instrutor: int
    instrutor: InstrutorOrNivel
    id_nivel: int
    nivel: InstrutorOrNivel
    avaliacao: mediaAvaliacao
    quantidade_avaliacoes: qtdAvaliacao
    preco: precoType

    class Config:
        from_attributes = True  # Pydantic v2 - converte objetos SQLAlchemy

class CursoEspecificoResponse(BaseModel):
    id: int
    titulo: tituloType
    descricao: descricaoType
    avaliacao: mediaAvaliacao
    quantidade_avaliacoes: qtdAvaliacao
    quantidade_horas: cargaHorariaType
    id_nivel: int
    nivel: InstrutorOrNivel
    preco: precoType
    id_instrutor: int
    instrutor: InstrutorOrNivel
    id_especialidade: int
    especialidade_instrutor: str

    class Config:
        from_attributes = True


##===================== CURSO - CONTROLE (ADMIN/INSTRUTOR) ========================##
# Contrato do front:
# POST /courses
# PUT  /courses/{id}
# DELETE /courses/{id}
# GET /courses/{id}/statistics

# Campos base para criação/atualização de curso
class CursoControleBase(BaseModel):
    """
    Campos base alinhados com o contrato do front para controle de cursos.
    Usado tanto na criação quanto na edição.
    """
    titulo: tituloType
    descricao: descricaoType                   # descrição curta do curso
    id_categoria: IdCategoriaType
    id_nivel: idNivelType
    id_instrutor: Optional[idInstrutorType] = None
    preco: PrecoOptionalType = 0.0            # float|null, default 0

# Schema de entrada quando o usuário está criando um curso
class CursoControleCriar(CursoControleBase):
    """
    Schema de entrada para criação de curso.
    POST /courses

    Regras de negócio:
    - se role = admin, pode enviar qualquer/nenhum id_instrutor
    - se role = instrutor, id_instrutor deve ser sobrescrito com o id do usuário logado
    """
    pass

# Schema de atualização quando o usuário está atualizando um curso
class CursoControleAtualizar(CursoControleBase):
    """
    Schema de entrada para edição de curso.
    PUT /courses/{id}

    O contrato do front inclui o "id" no body,
    então mantemos esse campo aqui.
    """
    id: int

# Schema de saída quando o usuário cria/edita um curso
class CursoControleResponse(CursoControleBase):
    """
    Schema de saída ao criar/editar um curso na área de controle.
    Respeita o contrato:

    {
        "id": int,
        "titulo": ...,
        "descricao": ...,
        "sobre": ...,
        "id_categoria": int,
        "id_nivel": int,
        "id_instrutor": int,
        "preco": float|null
    }
    """
    id: int
    sobre: float = 0.0  # média das notas, calculada pelo backend

    class Config:
        from_attributes = True


##===================== CURSOS - ESTATÍSTICAS ========================##
# Schema de saída para estatísticas de cursos
class CursoEstatisticaItem(BaseModel):
    """
    Item de estatística do curso.

    Contrato do front (resposta é um ARRAY de itens):
    [
        {
            "id": int,
            "titulo": string,
            "id_categoria": int,
            "categoria": string,
            "id_nivel": int,
            "nivel": string,
            "id_instrutor": int,
            "instrutor": string,
            "percentual_conclusao": float,
            "media_notas": float,
            "quantidade_alunos": int,
            "data_criacao": Date,
            "data_publicacao": Date
        }
    ]
    """
    id: int
    titulo: str
    id_categoria: int
    categoria: str
    id_nivel: int
    nivel: str
    id_instrutor: int
    instrutor: str
    percentual_conclusao: float
    media_notas: float
    quantidade_alunos: int
    data_criacao: datetime
    data_publicacao: Optional[datetime]

    class Config:
        from_attributes = True
