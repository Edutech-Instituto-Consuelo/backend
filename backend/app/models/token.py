from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class RefreshToken(Base):
    #Tabela para guardar os tokens de refresh

    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    token = Column(String, unique=True, index=True, index=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False) # Link com a tabela Usuarios

    # Aqui precisamos usar string "User" para evitar erro de importação se o User não estiver aqui
    usuario = relationship("Usuario", back_populates="refresh_tokens")

    # Monitorar possiveis ataques / logins vindos de ips suspeitos
    created_by_ip = Column(String, nullable=True)
    # Controle de qual dispositivo gerou aquele token
    user_agent = Column(String, nullable=True)
