from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.security import verify_token

PUBLIC_PATHS = {
	"/auth/login",
	"/auth/register",
}

def register_jwt_middleware(app):
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
