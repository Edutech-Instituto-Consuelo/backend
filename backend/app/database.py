# backend/app/database.py
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Lê a URL do banco de dados da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não foi definida. Verifique seu .env e docker-compose.")

# Cria o engine do SQLAlchemy apontado para o Supabase
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}, # reforça o SSL (além do ?sslmode=require na URL)
)

# Fábrica de sessões (para serem utilizadas nos serviços/repos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def test_connection():
    """
    Faz um SELECT 1 só pra testar se o banco está respondendo.
    Usaremos isso numa rota /db-check.
    """
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))