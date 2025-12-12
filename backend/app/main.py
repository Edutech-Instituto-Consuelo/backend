from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import middleware
from app.core.cors import setup_cors
from app.routers import auth, category, level, course, instructor
from app.routers import evaluation
import os

# importando a função de teste de conexão com Supabse
from .database import test_connection, Base, engine

Base.metadata.create_all(bind=engine)

# Instância básica da API
app = FastAPI(
    title="API de Teste - EduTech",
    description="API simulada apenas para testar Docker + Supabase",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

middleware.register_jwt_middleware(app)

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(level.router)
app.include_router(course.router)
app.include_router(instructor.router)
app.include_router(evaluation.router)

# Rota raiz
@app.get("/")
def root():
    return {"message": "API rodando com sucesso dentro do Docker"}

# Outra rota simples
@app.get("/status")
def status():
    return {"status": "ok", "docker": True, "backend": "online"}

# Rota para testar variáveis de ambiente de DB
import os
@app.get("/env")
def read_env():
    return {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
    }

# Rota para testar a conexão com o Supabse
@app.get("/db-check")
def db_check():
    try:
        test_connection()
        return {
            "db": "ok",
            "detail": "Conexão com Supabase funcionando!"
        }
    except Exception as e:
        return {
            "db": "error",
            "detail": str(e)
        }
