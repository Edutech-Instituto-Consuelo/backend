# backend/app/core/middleware.py
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from app.core.security import verify_token
import os

PUBLIC_PATHS = {
    "/auth/login",
    "/auth/register",
    "/courses",
    "/categories",
    "/levels",
}

if os.getenv("ENV", "development") == "development":
    PUBLIC_PATHS.update({
        "/docs",
        "/openapi.json",
        "/db-check",
        "/",
    })


def register_jwt_middleware(app):
    """Middleware global de validação JWT"""
    @app.middleware("http")
    async def jwt_middleware(request: Request, call_next):
        try:
            path = request.url.path
            normalized_path = path.rstrip("/") or "/"

            # 🔓 Rotas públicas fixas
            if normalized_path in PUBLIC_PATHS:
                return await call_next(request)

            # 🔓 Rotas públicas dinâmicas (GET)
            if request.method == "GET":
                # /courses/{id}
                if normalized_path.startswith("/courses/"):
                    parts = normalized_path.split("/")
                    if len(parts) == 3 and parts[2].isdigit():
                        return await call_next(request)

                    # /courses/{id}/modules (se público)
                    if len(parts) == 4 and parts[2].isdigit() and parts[3] == "modules":
                        return await call_next(request)

                # /courses/{id}/reviews
                if normalized_path.startswith("/courses/") and normalized_path.endswith("/reviews"):
                    return await call_next(request)

            # 🔐 Rotas protegidas
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token não fornecido."
                )

            token = auth_header.split(" ")[1]
            user_data = verify_token(token)
            request.state.user = user_data

            return await call_next(request)

        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail}
            )

#		except Exception as e:
#			return JSONResponse(
#				status_code=500,
#				content={"detail": "Erro interno no servidor."}
#			)
