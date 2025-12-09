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

def allowed_roles(*list_roles:str):
	"""Função que funciona como um decorador no fastAPI, deve ser usada atraves de um Depends nas rotas

	Exemplo de uso: Depens(allowed_roles("aluno", "admin", "instrutor")).
	Todas as roles passadas no argumentos serão autorizadas, se não passar nada, todas tem acesso
	"""
	def dependency(request: Request) -> dict:
		"""Função dependencia que retorna dicionario com os dados do payload do usuario"""
		user = request.state.user
		role = user.get("role")
		print(role)
		if list_roles and role not in list_roles:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Role não permitida"
			)
		return user
	return dependency
