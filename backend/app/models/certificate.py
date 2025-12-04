from uuid import uuid4
from sqlalchemy import (
    Column, Integer, DateTime, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base

class Certificado(Base):
    """
    Modelo Certificado
    ------------------
    Representa a tabela 'certificados' no banco de dados.
    Cada certificado está associado a uma matrícula específica e contém detalhes sobre a emissão do certificado.
    """

    # NOME DA TABELA
    __tablename__ = "certificados"

    # COLUNAS
    id = Column(
        UUID(as_uuid=True),
        primary_key=True, 
        default=uuid4,
        index=True,
    )

    # CHAVE ESTRANGEIRA
    matricula_id = Column(
        Integer,
        ForeignKey("matriculas.id"),
        nullable=False,
        unique=True, # Um certificado por matrícula
    )

    # DETALHES DO CERTIFICADO
    data_conclusao = Column(
        DateTime(timezone=True),
        nullable=False,
    )

    data_emissao = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    # RELACIONAMENTOS
    # Matrícula 1:1 → Cada matrícula possui um único certificado vinculado
    matricula = relationship(
        "Matricula",
        back_populates="certificado",
    )