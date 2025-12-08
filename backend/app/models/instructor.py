from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Instrutor(Base):
    """
    Modelo Instrutor
    ---------------
    Representa a tabela 'instrutores'no banco de dados.
    Cada instrutor está vinculado a um usuário (tabela 'usuarios')
    e poderá ter vários cursos associados.
    """

    __tablename__="instrutores"

    # ID do instrutor
    # - chave primária da tabela 'instrutores'
    # - chave estrangeira para 'usuarios.id' (1:1 com Usuario)
    id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        primary_key=True,
        index=True,
    )

    # Especialidade do instrutor (FK para tabela 'especialidade')
    # Ex.: BackEnd, Data Science, UX, etc..
    especialidade = Column(
        Integer,
        ForeignKey("especialidade.id"),
        nullable=False,
    )

    # Biografia do instrutor (resumo do perfil profissional)
    biografia = Column(String(300), nullable=True)

    # Data em que o instrutor foi cadastrado
    data_cadastro = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Data da última atualização dos dados do instrutor
    ultima_alteracao = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # RELACIONAMENTOS
    # Relacionamento 1:1 com Usuarios
    # Um instrutor está associado a um usuário
    usuario = relationship(
        "Usuario",
        back_populates="instrutor",
    )

    # Relacionamento 1:N com Curso
    # Um instrutor pode ter vários cursos cadastrados na plataforma
    cursos = relationship(
        "Curso",
        back_populates="instrutor",
        cascade="all, delete-orphan"
    )

    especialidade_rel = relationship(
        "Especialidade",
        back_populates="instrutores",
    )