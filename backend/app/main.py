from fastapi import FastAPI

# Instância básica da API
app = FastAPI(
    title="API de Teste - EduTech",
    description="API simulada apenas para testar Docker + Compose",
    version="1.0.0"
)

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
        "DB_HOST": os.getenv("DB_HOST"),
        "DB_PORT": os.getenv("DB_PORT"),
        "DB_NAME": os.getenv("DB_NAME")
    }
