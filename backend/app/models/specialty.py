from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Especialidade(Base):
    """
    Modelo Especialidade
    --------------------
    Representa a especialidade de um instrutor,
    como por exemplo: Back-end, Front-end, Dados, UX, etc.
    """

    __tablename__ = "especialidade"

    id = Column(Integer, primary_key=True, index=True)

    # Nome da especialidade (ex.: "Back-end", "Ciência de Dados")
    nome = Column(String(100), nullable=False, unique=True)

    # Descrição opcional da especialidade
    descricao = Column(Text, nullable=True)

    # Relacionamento 1:N com Instrutor
    instrutores = relationship(
        "Instrutor",
        back_populates="especialidade_rel",
        cascade="all, delete-orphan",
    )
