from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
#from sqlalchemy.dialects.postgresql import CITEXT
from sqlalchemy.orm import relationship
from app.database import Base # onde Base = declarative_base()


class Usuario(Base):
    # Modelo do Usuario

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(45), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    senha_hash = Column(String(255), nullable=False)
    tipo_usuario =  Column(String(20), nullable=False, default="aluno")
    data_nascimento = Column(Date, nullable=False)
    data_cadastro = Column(DateTime, nullable=False, server_default=func.now())
    ultimo_login = Column(DateTime, nullable=True)

    # Relacionamento 1:1 com Instructor.
    # Se o usuário for do tipo "instrutor", este atributo aponta
    # para o registro correspondente na tabela 'instrutores'.
    instrutor = relationship(
        "Instrutor",
        back_populates="usuario",
        uselist=False,  # garante relação 1:1
    )

    # Relacionamento 1:N com Matricula.
    # Um usuário (aluno) pode ter muitas matrículas.
    matriculas = relationship(
        "Matricula",
        back_populates="aluno",
        cascade="all, delete-orphan",
    )
