from sqlalchemy import (Column, Integer, String, Text, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Avaliacao(Base):
    """
    Modelo Avaliacao
    --------------
    Representa a tabela 'avaliacoes' no banco de dados
    Cada avaliação está associada a um curso e a um usuário.
    """

    # NOME DA TABELA
    __tablename__ = "avaliacoes"

    # COLUNAS
    id = Column(Integer, primary_key=True, index=True)
    nota = Column(Integer, nullable=False)  # Nota da avaliação (1-5)
    comentario = Column(Text, nullable=True)  # Comentário opcional do usuário

    # CHAVES ESTRANGEIRAS
    curso_id = Column(
        Integer, 
        ForeignKey("cursos.id"), 
        nullable=False
    )

    usuario_id = Column(
        Integer, 
        ForeignKey("usuarios.id"), 
        nullable=False
    )

    # CONTROLE DE DATA/HISTÓRICO
    data_criacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    # RELACIONAMENTOS
    # Curso 1:N → Um curso pode ter muitas avaliações
    curso = relationship(
        "Curso",
        back_populates="avaliacoes",
    )

    # Usuário 1:N → Um usuário pode fazer muitas avaliações
    usuario = relationship(
        "Usuario",
        back_populates="avaliacoes",
    )