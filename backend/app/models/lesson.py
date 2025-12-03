from sqlalchemy import (
    Column, Integer, String,
    Text, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Aula(Base):
    """
    Modelo Aula
    ---------------
    Representa a tabela 'aulas' no banco de dados.
    Cada aula pertence a um módulo específico de um curso.
    """

    # NOME DA TABELA
    __tablename__ = "aulas"

    # COLUNAS
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)

    # Detalhes da aula
    ordem_aula = Column(Integer, nullable=False)        # Ordem da aula dentro do módulo
    duracao_minutos = Column(Integer, nullable=False)   # Duração em minutos
    tipo = Column(String(50), nullable=False)           # Tipo de aula (vídeo, texto, quiz, etc.)

    # Opcional:
    # subtitulo com breve resumo da aula
    subtitulo = Column(Text, nullable=True) 

    # CHAVE ESTRANGEIRA
    modulo_id = Column(
        Integer,
        ForeignKey("modulos.id"),
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
    # Módulos 1:N → Um módulo contém muitas aulas
    modulo = relationship(
        "Modulo",
        back_populates="aulas",
    )

    # Progresso 1:N → Uma aula pode ter muitos registros de progresso
    progresso_aulas = relationship(
        "ProgressoAulas",
        back_populates="aula",
        cascade="all, delete-orphan",
    )