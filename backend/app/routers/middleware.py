from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.security import verify_token
import os

PUBLIC_PATHS = {
	"/auth/login",
	"/auth/register",
}

"""
	Verificação do tipo de env, basicamente se no .env estiver explicito algo diferente de development ele não adiciona a public_paths as seguintes rotas.
	Obs(não necessita colocar na env, pois caso não tenha nada ele considera como development por padrão).
"""

if os.getenv("ENV", "development") == "development":
	PUBLIC_PATHS.update({
		"/docs",
		"/openapi.json",
		"/db-check",
		"/",
	})

def register_jwt_middleware(app):
	"""
		Este middleware intercepta todas as requisições HTTP e realiza as seguintes ações:
		1. Permite acesso direto às rotas públicas definidas em PUBLIC_PATHS.
		2. Verifica se o header 'Authorization' está presente e no formato 'Bearer <token>'.
		3. Valida o token JWT utilizando a função `verify_token`.
		4. Armazena os dados do usuário presentes no playload como `request.state.user` para uso nos endpoints.
		5. Trata erros de autenticação retornando HTTP 401 e erros internos retornando HTTP 500.
	"""
	@app.middleware("http")
	async def jwt_middleware(request: Request, call_next):
		try:
			path = request.url.path

			if path in PUBLIC_PATHS:
				return await call_next(request)

			auth_header = request.headers.get("Authorization")

			if not auth_header or not auth_header.startswith("Bearer "):
				raise HTTPException(
					status_code=status.HTTP_401_UNAUTHORIZED,
					detail="Token não fornecido.")

			token = auth_header.split(" ")[1]
			user_data = verify_token(token)
			request.state.user = user_data
			return await call_next(request)

		except HTTPException as e:
			return JSONResponse(
				status_code=e.status_code,
				content={"detail": e.detail}
			)
		except Exception as e:
			return JSONResponse(
				status_code=500,
				content={"detail": "Erro interno no servidor."}
			)
