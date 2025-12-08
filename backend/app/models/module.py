from sqlalchemy import (
    Column, Integer, DateTime,
    String, Text, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Modulo(Base):
    """
    Modelo Modulo
    --------------
    Representa a tabela 'modulos' no banco de dados.
    Cada módulo pertence a um curso e agrupa um conjunto de aulas.
    """

    # NOME DA TABELA
    __tablename__ = 'modulos'

    # COLUNAS BÁSICAS
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=True)

    # ordem do módulo dentro do curso (ex: Módulo 1, Módulo 2, etc.)
    ordem = Column(Integer, nullable=False)
    
    # CHAVES ESTRANGEIRAS
    curso_id = Column(
        Integer,
        ForeignKey('cursos.id'),
        nullable=False,
    )

    # CONTROLE DE DATA/HISTÓRICO
    data_criacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    ultima_atualizacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # RELACIONAMENTOS
    # Cursos 1:N → Um curso pode conter muitos módulos
    curso = relationship(
        "Curso",
        back_populates="modulos",
    )

    # Aulas N:1 → Um módulo pode conter muitas aulas
    aulas = relationship(
        "Aula",
        back_populates="modulo",
        cascade="all, delete-orphan"
    )
