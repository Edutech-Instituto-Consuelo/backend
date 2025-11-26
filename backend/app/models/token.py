from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class RefreshToken(Base):
    #Tabela para guardar os tokens de refresh

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    revoked_at = Column(DateTime, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id")) # Link com a tabela Usuarios

    # Aqui precisamos usar string "User" para evitar erro de importação se o User não estiver aqui
    usuario = relationship("Usuario", back_populates="refresh_tokens")
