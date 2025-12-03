from fastapi import APIRouter, Depends, status, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import create_salt, verify_password, get_password_hash
from app.core.security import get_current_user
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import Usuario
from app.schemas.user import UsuarioCriar, UsuarioResponse, TokenResponse, UsuarioLogin
from app.schemas.user import UsuarioLogin
from typing import List
from app.core.security import create_access_token


router = APIRouter(
	prefix="/auth",
	tags=["Auth"]
)

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
		senha_hash = get_password_hash(create_salt(usuario.senha_hash, usuario.email)),
		tipo_usuario = usuario.tipo_usuario,
		data_nascimento = usuario.data_nascimento
	)

	db.add(db_usuario)
	db.commit()
	db.refresh(db_usuario)
	return db_usuario

@router.get("/usuarios", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
	"""Função que retorna todos os usuarios cadastrados"""
	query = db.query(Usuario)

	return query

# Rota de login
"""
	Recebo dados em json do front. Padrão email e senha como definido no shema user UsuarioLogin.
	Depois busco no banco algum usuario que tenha o mesmo email, verifico se consigo achar,
	se conseguir verifico a senha e caso esteja errado retorn erro pro front. Caso esetja certo gero
	o token e retorno o mesmo para o front.
"""
@router.post("/login", response_model=TokenResponse)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
	user = db.query(Usuario).filter(Usuario.email == data.email).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Credenciais inválidas"
			)

	senha_com_salt = create_salt(data.senha, user.email)
	if not verify_password(senha_com_salt, user.senha_hash):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Credenciais inválidas"
			)

	token = create_access_token(user_id=user.id, email=user.email)
	print("to aqui")
	return {"access_token": token}
