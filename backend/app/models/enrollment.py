from sqlalchemy import (
    Column, Integer, String, 
    Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Matricula(Base):
    """
    Modelo Matricula
    -----------------
    Representa a tabela 'matriculas' no banco de dados.
    Cada matrícula registra a participação de um aluno em um curso específico, incluindo status e datas.
    """
    # NOME DA TABELA
    __tablename__ = "matriculas"

    # COLUNAS
    id = Column(Integer, primary_key=True, index=True)

    # CHAVES ESTRANGEIRAS
    aluno_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )
    curso_id = Column(
        Integer,
        ForeignKey("cursos.id"),
        nullable=False
    )

    # CONTROLE DE DATA/HISTÓRICO
    data_matricula = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    # Estado da matrícula, pode ser ativa, cancelada, concluida
    status_matricula = Column(String(12), nullable=False, default="ativa")
    data_conclusao = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    # RELACIONAMENTOS
    # Aluno 1:N → Um aluno pode ter muitas matrículas
    aluno = relationship(
        "Usuario",
        back_populates="matriculas",
    )

    # Curso 1:N → Um curso pode ter muitas matrículas
    curso = relationship(
        "Curso",
        back_populates="matriculas",
    )

    # Avaliações 1:N → Uma matrícula pode ter muitas avaliações
    avaliacoes = relationship(
        "DesempenhoAluno",
        back_populates="matricula",
        cascade="all, delete-orphan",
    )

    # Progresso 1:N → Uma matrícula tem o progresso de várias aulas
    progresso_aulas = relationship(
        "ProgressoAulas",
        back_populates="matricula",
        cascade="all, delete-orphan",
    )

    # Certificado 1:1 → Uma matrícula tem um certificado
    certificado = relationship(
        "Certificado",
        back_populates="matricula",
        uselist=False,
        cascade="all, delete-orphan",
    )