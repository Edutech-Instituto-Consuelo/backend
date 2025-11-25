from passlib.hash import pbkdf2_sha256

def get_password_hash(password: str) -> str:
	"""
	Função que recebe uma string(senha) e retorna o hash da string
	"""
	return pbkdf2_sha256.hash(password)

def create_salt(senha: str , email:str) -> str:
	"""Função que retorna o salt da senha"""
	nova_senha = senha
	for i in range(10):
		nova_senha += email[i]

	return nova_senha

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pbkdf2_sha256.verify(plain_password, hashed_password)
