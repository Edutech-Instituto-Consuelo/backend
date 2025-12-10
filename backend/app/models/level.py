from app.database import Base
from sqlalchemy import Column, Integer, String

class Nivel(Base):

	__tablename__="niveis"

	id = Column(
		Integer,
		primary_key=True,
		index=True,
		autoincrement=True)
	descricao =  Column(String(20), nullable=False, unique=True)
