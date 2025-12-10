from app.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Nivel(Base):

	__tablename__="niveis"

	id = Column(
		Integer,
		primary_key=True,
		index=True,
		autoincrement=True)
	descricao =  Column(String(20), nullable=False, unique=True)

	cursos = relationship(
		"Curso",
		back_populates="nivel",
		cascade="all, delete-orphan"
	)
