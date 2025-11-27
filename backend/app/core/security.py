# app/core/security.py
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import Usuario
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(user_id: int, email: str):

	expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

	payload = {
		"sub": str(user_id),
		"email": email,
		"exp": expire
	}

	# jwt.encode = cria a string JWT segura e assinada
	token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

	return token

def verify_token(token: str):
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

		user_id = payload.get("sub")
		email = payload.get("email")
		exp = payload.get("exp")
		return {"id": int(user_id), "email": email, "exp": exp}

	except JWTError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token inválido ou expirado.")

def get_current_user(token: str, db: Session = Depends(get_db)):
	data = verify_token(token)

	user = db.query(Usuario).filter(Usuario.id == data["id"]).first()
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Usuário não encontrado.")

	return user
