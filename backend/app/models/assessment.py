from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class DesempenhoAluno(Base):
    """
    Modelo DesempenhoAluno
    -----------------
    Representa a tabela 'desempenho' no banco de dados.
    Cada desempenho está associado a uma matrícula específica e contém a nota e feedback sobre o aluno.
    """

    # NOME DA TABELA
    __tablename__ = "desempenho"

    # COLUNAS
    id = Column(Integer, primary_key=True, index=True)

    # CHAVES ESTRANGEIRAS
    matricula_id = Column(
        Integer,
        ForeignKey("matriculas.id"),
        nullable=False
    )

    # DETALHES DA AVALIAÇÃO
    nota = Column(Integer, nullable=False)          # Nota da avaliação (0-100)
    comentario = Column(String(500), nullable=True)   # Comentários adicionais

    # CONTROLE DE DATA/HISTÓRICO
    data_avaliacao = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # RELACIONAMENTOS
    # Matrícula 1:N → Uma matrícula pode ter muitas avaliações
    matricula = relationship(
        "Matricula",
        back_populates="avaliacoes",

    ) 