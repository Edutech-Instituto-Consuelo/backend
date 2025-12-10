from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Curso(Base):
    """
    Modelo Curso
    --------------
    Representa a tabela 'cursos' no banco de dados
    Cada curso pertence a uma categoria específica e é ministrado por um instrutor.
    """

    # NOME DA TABELA
    __tablename__ = "cursos"

    # COLUNAS
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    descricao = Column(Text, nullable=False)
    nivel = Column(String(50), nullable=False)  # Iniciante, Intermediário, Avançado
    preco = Column(Float, nullable=False)
    carga_horaria = Column(Integer, nullable=False)  # em horas

    # CHAVES ESTRANGEIRAS
    nivel_id = Column(
        Integer,
        ForeignKey("niveis.id"),
        nullable=False
    )
    categoria_id = Column(
        Integer,
        ForeignKey("categorias.id"),
        nullable=False
    )

    instrutor_id = Column(
        Integer,
        ForeignKey("instrutores.id"),
        nullable=False
    )

    # CONTROLE DE DATA/HISTÓRIOC
    data_criacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    ultima_atualizacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    # RELACIONAMENTOS
    # Nivel 1:N -> um nivel em varios cursos
    nivel = relationship(
        "Nivel",
        back_populates="cursos",
    )

    # Instrutor 1:N → Um instrutor pode ministrar muitos cursos
    instrutor = relationship(
        "Instrutor",
        back_populates="cursos",
    )

    # Categoria 1:N → Uma categoria pode ter muitos cursos
    categoria = relationship(
        "Categoria",
        back_populates="cursos",
    )

    # Matriculas 1:N → Um curso pode ter muitas matrículas
    matriculas = relationship(
        "Matricula",
        back_populates="curso",
        cascade="all, delete-orphan",
    )

    # Modulos 1:N → Um curso pode ter muitos módulos
    modulos = relationship(
        "Modulo",
        back_populates="curso",
        cascade="all, delete-orphan",
    )
