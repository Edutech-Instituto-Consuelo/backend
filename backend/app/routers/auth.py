from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.app.database import get_db
from passlib.hash import pbkdf2_sha256
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from backend.app.models.user import Usuario
from backend.app.schemas.user import UsuarioCriar, UsuarioResponse
from typing import List


router = APIRouter(
	prefix="/auth",
	tags=["Auth"]
)

def get_password_hash(password: str) -> str:
	"""
	Função que recebe uma string(senha) e retorna o hash da string
	"""
	return pbkdf2_sha256.hash(password)

@router.post("/register", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registra_usuario(
	usuario: UsuarioCriar, db: Session = Depends(get_db)
):
	"""Função que registra o usuario no banco"""

	ja_existe = db.query(Usuario).filter(
		Usuario.email == usuario.email
	).first()

	if ja_existe:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="Usuario ja cadastrado!"
		)
	db_usuario = Usuario(
		nome = usuario.nome,
		email = usuario.email,
		senha_hash = get_password_hash(usuario.senha_hash),
		tipo_usuario = usuario.tipo_usuario,
		data_nascimento = usuario.data_nascimento
	)

	db.add(db_usuario)
	db.commit()
	db.refresh(db_usuario)
	return db_usuario

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(
	db: Session = Depends(get_db)
):
	"""Função que retorna todos os usuarios cadastrados"""
	query = db.query(Usuario)

	return query

