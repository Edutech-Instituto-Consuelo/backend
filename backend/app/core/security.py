# app/core/security.py
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Usuario
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


# Função na qual gera o token JWT e retorna o mesmo
def create_access_token(user_id: int, email: str , role: str):

	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

	payload = {
		"sub": str(user_id),
		"email": email,
		"role" : role,
		"exp": expire
	}

	# jwt.encode = cria a string JWT segura e assinada
	token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

	return token

# Função para verificar se o token é valido
def verify_token(token: str):
	try:
		'''
		Decode decodifica o payload e header do token cria um novo a partir da secret key e verifica se os 2 batem.
		E verifica algumas coisas a mais também como por exemplo campo exp (referente ao tem de expiração do token),
		Caso de erro ele da um erro e eu trato isso apartir do JWTError que pega qualquer erro saindo do decode basicamente.
		'''
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

		user_id = payload.get("sub")
		email = payload.get("email")
		role = payload.get("role")
		exp = payload.get("exp")
		return {"id": int(user_id), "email": email, "role": role, "exp": exp}

	except JWTError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido ou expirado.")


def allowed_roles(*list_roles: str):
    """
    Função que funciona como um decorador no FastAPI, deve ser usada através de um Depends nas rotas.

    Exemplo de uso:
        Depends(allowed_roles("aluno", "admin", "instrutor"))

    Todas as roles passadas nos argumentos serão autorizadas.
    Se não passar nada, qualquer role autenticada tem acesso.
    """
    def dependency(request: Request) -> dict:
        """
        Função dependência que retorna um dicionário com os dados do payload do usuário.
        Primeiro tenta usar o que o middleware colocou em request.state.user.
        Se não houver, faz o parse do header Authorization aqui mesmo.
        """

        # 1) Tenta pegar o usuário setado pelo middleware
        user = getattr(request.state, "user", None)

        # 2) Se o middleware não setou, tentamos extrair o token direto do header
        if user is None:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token não fornecido."
                )

            token = auth_header.split(" ", 1)[1]
            user = verify_token(token)

        role = user.get("role")
        print(role)

        # 3) Se foi passada uma lista de roles, validamos se a role do usuário é permitida
        if list_roles and role not in list_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Role não permitida"
            )

        return user

    return dependency
