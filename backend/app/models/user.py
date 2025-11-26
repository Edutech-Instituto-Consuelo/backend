from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.sql import func
#from sqlalchemy.dialects.postgresql import CITEXT
from backend.app.database import Base # onde Base = declarative_base()




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
    
    #Caso queira deletar um usuario, todos os tokens de refresh associados a ele também serão deletados
    refresh_tokens = relationship("RefreshToken", back_populates="usuario", cascade="all, delete-orphan")