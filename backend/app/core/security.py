# app/core/security.py
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Usuario
from app.core.config import JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY


# Função na qual gera o token JWT e retorna o mesmo
def create_access_token(user_id: int, email: str):
	print("antes")
	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	print(expire)
	payload = {
		"sub": str(user_id),
		"email": email,
		"exp": expire.timestamp()
	}
	print(payload)

	# jwt.encode = cria a string JWT segura e assinada

	print(JWT_SECRET_KEY)
	token = jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
	print("aaaaaaa")

	print("depois")
	print(token)
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
		exp = payload.get("exp")
		return {"id": int(user_id), "email": email, "exp": exp}

	except JWTError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido ou expirado.")

# Função que verifica token e pega o objeto user no banco e retorna o mesmo
def get_current_user(token: str, db: Session = Depends(get_db)):
	data = verify_token(token)

	user = db.query(Usuario).filter(Usuario.id == data["id"]).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuário não encontrado.")

	return user
