from sqlalchemy import (
    Column, Integer, String,
    DateTime, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base # onde Base = declarative_base()


class Usuario(Base):
    """
    Modelo Usuario
    ---------------
    Representa a tabela 'usuarios' no banco de dados.
    Armazena dados de identificação, autenticação e perfil do usuário.
    """
    # NOME DA TABELA
    __tablename__ = "usuarios"

    # COLUNAS
    # Informações básicas do usuário
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    nome = Column(String(45), nullable=False)
    sobrenome = Column(String(45), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)

    # Perfil do usuário
    tipo_usuario =  Column(String(20), nullable=False, default="aluno")

    # CONTROLE DE DATA/HISTÓRICO
    # data de criação do registro do usuário
    data_cadastro = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # data do último login autenticado pelo usuário
    ultimo_login = Column(
        DateTime,
        nullable=True,
    )

    # data da última atualização do perfil do usuário
    ultima_atualizacao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # RELACIONAMENTOS
    # Instrutor 1:1
    # Se o usuário for do tipo "instrutor", este atributo aponta
    # para o registro correspondente na tabela 'instrutores'.
    instrutor = relationship(
        "Instrutor",
        back_populates="usuario",
        uselist=False,  # garante relação 1:1
    )

    # Matricula 1:N → Um aluno pode ter várias matrículas
    matriculas = relationship(
        "Matricula",
        back_populates="aluno",
        cascade="all, delete-orphan",
    )

    avaliacoes_curso = relationship(
        "AvaliacaoCurso",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )
