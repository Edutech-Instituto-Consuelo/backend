from sqlalchemy import (
    Column, Integer, Boolean, 
    DateTime, ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import relationship

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
    # Percentual de progresso na aula (0-100)
    progresso_percentual = Column(
        Integer,
        nullable=False,
        default=0,
    )   
    # Indica se a aula foi concluída
    concluido = Column(
        Boolean,
        nullable=False,
        default=False,  
    )
    # Data de conclusão da aula, preenchida quando a aula é marcada como concluída
    data_conclusao = Column(
        DateTime(timezone=True),
        nullable=True,
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