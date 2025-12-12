from fastapi import APIRouter, Depends, status, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import create_salt, verify_password, get_password_hash
from app.core.security import allowed_roles

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
		sobrenome = usuario.sobrenome,
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
def listar_usuarios(db: Session = Depends(get_db) , require = Depends(allowed_roles("admin"))):
	"""Função que retorna todos os usuarios cadastrados"""
	query = db.query(Usuario)

	return query

# Rota de login

@router.post("/login", response_model=TokenResponse)
def login(data: UsuarioLogin, db: Session = Depends(get_db)):
	"""
	Recebo dados em json do front. Padrão email e senha como definido no shema user UsuarioLogin.
	Depois busco no banco algum usuario que tenha o mesmo email, verifico se consigo achar,
	se conseguir verifico a senha e caso esteja errado retorn erro pro front. Caso esetja certo gero
	o token e retorno o mesmo para o front.
	"""
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

	token = create_access_token(user_id=user.id, email=user.email, role=user.tipo_usuario)
	return {"access_token": token}

# Rota para obter informações do usuário autenticado
@router.get("/me", response_model=UsuarioResponse)
def get_me(db:Session = Depends(get_db), usuario = Depends(allowed_roles())):
	"""Rota para obter informações do usuário autenticado"""
	user = db.query(Usuario).filter(Usuario.id == usuario["id"]).first()
	return user


# Rota para solicitar redefinicao de senha.
#recebe o email, verifica se existe e gera um token que sera enviado por email.
@router.post("/recover", status_code=status.HTTP_200_OK)
def recuperar_senha(
    dados: Recuperacaodesenha, 
    db: Session = Depends(get_db)
):
    user = db.query(Usuario).filter(Usuario.email == dados.email).first()

    if user:
        print(f"DEBUG: Simulação de envio de email para {user.email}")
        pass
    return {"msg": "Você receberá um link de recuperação via email."}


# Rota POST: confirmar redefinicao de senha.
# Recebe o token (vindo do e-mail) e a nova senha, valida e atualiza no banco.
@router.post("/recover/confirm", status_code=status.HTTP_200_OK)
def confirmar_recuperacao(
    dados: Novasenha, 
    db: Session = Depends(get_db)
):  

    # Busca usuário no banco
    user = db.query(Usuario).filter(Usuario.email == email_usuario_simulado).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Cria nova hash de senha
    senha_com_salt = create_salt(dados.nova_senha, user.email)
    novo_hash = get_password_hash(senha_com_salt)

    # 4. Atualizar e Salvar
    user.senha_hash = novo_hash
    db.commit()

    return {"msg": "Senha alterada com sucesso!"}


# Rota renova token de autentificacao sem a necessidade de fazer login novamente.
@router.get("/refresh", response_model=TokenResponse)
def refresh_token(
    usuario_atual = Depends(allowed_roles()) 
):
    	novo_token = create_access_token(
        user_id=usuario_atual["id"], 
        email=usuario_atual["email"], 
        role=usuario_atual["role"] # ou 'tipo_usuario' dependendo de como retorna
    )
	return {"access_token": novo_token}