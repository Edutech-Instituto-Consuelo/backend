from pydantic import BaseModel, Field, conint
from typing import Optional, Annotated
from datetime import datetime

# Tipos anotados com validações
NotaType = Annotated[int, Field(ge=1, le=5, description="Nota da avaliação (1-5)")]
ComentarioType = Annotated[Optional[str], Field(max_length=500, description="Comentário opcional")]

##===================== AVALIACAO ========================##

# Campos base (sem id, sem data_criacao)
class AvaliacaoBase(BaseModel):
    nota: NotaType
    comentario: ComentarioType = None

# Schema de entrada quando o usuário está criando uma avaliação
class AvaliacaoCriar(AvaliacaoBase):
    curso_id: int
    usuario_id: int

# Schema de saída, aquilo que o servidor retorna ao consultar uma avaliação
class AvaliacaoResponse(AvaliacaoBase):
    id: int
    curso_id: int
    usuario_id: int
    data_criacao: datetime

    class Config:
        from_attributes = True  # Pydantic v2 - converte objetos SQLAlchemy

# Schema opcional para atualização parcial (PATCH)
# class AvaliacaoAtualizar(BaseModel):
#    """Usado em PATCH: todos opcionais"""
#    nota: Optional[NotaType] = None
#    comentario: Optional[str] = None
