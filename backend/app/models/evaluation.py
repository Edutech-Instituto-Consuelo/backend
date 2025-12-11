from sqlalchemy import (Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, CheckConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class AvaliacaoCurso(Base):
    """
    Modelo AvaliacaoCurso
    --------------
    Representa a tabela 'avaliacao_curso' no banco de dados
    Cada avaliação está associada a um curso e a um usuário.
    """

    # NOME DA TABELA
    __tablename__ = "avaliacao_curso"

    # RESTRIÇÕES
    __table_args__ = (
        # Restrição para evitar múltiplas avaliações do mesmo usuário para o mesmo curso
        UniqueConstraint('usuario_id', 'curso_id', name='uc_usuario_curso_avaliacao'),
        # Restrição para garantir que a nota esteja entre 1 e 5
        CheckConstraint('nota >= 1 AND nota <= 5', name='check_nota_range'),
    )

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
        back_populates="avaliacoes_curso",
    )

    # Usuário 1:N → Um usuário pode fazer muitas avaliações
    usuario = relationship(
        "Usuario",
        back_populates="reviews_curso",
    )
