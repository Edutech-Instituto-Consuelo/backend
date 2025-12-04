from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship # para criar relacionamentos ORM
from app.database import Base

class Categoria(Base):
    """
    Modelo Categoria
    --------------
    Representa a tabela 'categorias' no banco de dados
    Cada categoria agrupa cursos semelhantes (ex.: Tecnologia, Design, Marketing)
    """

    # NOME DA TABELA
    __tablename__="categorias"                              

    # COLUNAS
    # ID único por categoria
    id = Column(Integer, primary_key=True, index=True)
    
    # Nome, único pra não ter categoria duplicada
    nome = Column(String(100), nullable=False, unique=True) 
    
    # Descrição da categoria
    descricao = Column(Text, nullable=False)

    # RELACIONAMENTO 1:N → Uma categoria pode ter vários cursos
    # Relacionamento com courses. 
    # O 'back_populates' deve corresponder ao atributo 'categoria' de dentro do model "Course"
    cursos = relationship(
        "Curso", 
        back_populates="categoria",
        cascade="all, delete-orphan",
        # permite deletar cursos quando a categoria for removida. 
    )