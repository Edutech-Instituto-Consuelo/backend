#from app.routers.auth import create_salt, get_password_hash
from passlib.hash import pbkdf2_sha256

def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pbkdf2_sha256.verify(plain_password, hashed_password)

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

senha = "string"
email = "user1@gmail.com"

new_str = create_salt(senha, email)
print(senha)
print(new_str)

outra_senha = senha

hash_senha = get_password_hash(senha)
hash_senha1 = get_password_hash(outra_senha)
hash_new_str = get_password_hash(new_str)

print(verify_password(outra_senha, hash_senha))
print(verify_password(senha, hash_senha1))
