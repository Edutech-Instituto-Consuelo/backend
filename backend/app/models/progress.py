from sqlalchemy import (
    Column, Integer, Boolean, 
    DateTime, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class ProgressoAulas(Base):
    """
    Modelo ProgressoAulas
    ---------------------
    Representa a tabela 'progresso_aulas' no banco de dados.
    Cada registro indica o progresso de um aluno em uma aula específica dentro de um módulo.
    """

    # NOME DA TABELA
    __tablename__ = "progresso_aulas"

    # CHAVE PRIMÁRIA COMPOSTA
    __table_args__ = (
        PrimaryKeyConstraint('matricula_id', 'aula_id'),
    )

    # CHAVES ESTRANGEIRAS
    matricula_id = Column(
        Integer,
        ForeignKey("matriculas.id"),
        nullable=False
    )
    aula_id = Column(
        Integer,
        ForeignKey("aulas.id"),
        nullable=False
    )

    # DETALHES DO PROGRESSO
    concluido = Column(Boolean, nullable=False, default=False)          # Indica se a aula foi concluída
    progresso_percentual = Column(Integer, nullable=False, default=0)   # Percentual de progresso na aula (0-100)

    # CONTROLE DE DATA/HISTÓRICO
    data_ultimo_acesso = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # RELACIONAMENTOS
    # Matrícula 1:N → Uma matrícula pode ter muitos registros de progresso
    matricula = relationship(
        "Matricula",
        back_populates="progresso_aulas",
    )

    # Aula 1:N → Uma aula pode ter muitos registros de progresso
    aula = relationship(
        "Aula",
        back_populates="progresso_aulas",
    )