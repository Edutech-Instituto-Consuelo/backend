from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class StatusCurso(Base):
    """
    Modelo Status de publicação do curso
    --------------
    Representa a tabela 'status_cursos' no banco de dados
    Cada curso possui um status de publicação.
    """

    # NOME DA TABELA
    __tablename__ = "status_curso"


    #COLUNAS
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(200), nullable=True) #Rascunho, publicado, Descontinuado


    #RELACIONAMENTOS
    cursos = relationship(
        "Curso",
        back_populates="status",
    )
