"""
Configuração central de conexão com o banco de dados usando SQLAlchemy.

Este arquivo é responsável por:
- Ler a variável de ambiente `DATABASE_URL` (vinda do .env ou do docker-compose)
- Criar o `engine`, que é a conexão principal com o banco (no nosso caso, Supabase/PostgreSQL)
- Criar a fábrica de sessões (`SessionLocal`), utilizada pelas rotas e serviços. Não cria a conexão diretamente, mas sim sessões "sob demanda" a partir de um modelo de sessão.
- Definir a `Base` para todos os modelos ORM do projeto, ou sejo, o modelo "mãe" de todas as tabelas.
- Disponibilizar uma função de teste (`test_connection`) para validar a comunicação com o banco

Toda parte do backend que precisa acessar o banco utilizará estes componentes.
"""

import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Lê a URL do banco de dados da variável de ambiente
#DATABASE_URL ="postgresql://gabriel:Dragonoide01@host.docker.internal:5432/edutech"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não foi definida. Verifique seu .env e docker-compose.")

# Cria o engine do SQLAlchemy apontado para o Supabase
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={
        "sslmode": "require",
        "options": "-c inet_server_family=4"}, # reforça o SSL (além do ?sslmode=require na URL)
)

# Fábrica de sessões (para serem utilizadas nos serviços/repos)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos ORM
Base = declarative_base()

def test_connection():
    """
    Faz um SELECT 1 só pra testar se o banco está respondendo.
    Usaremos isso numa rota /db-check.
    """
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

def get_db():
    """
    Função que cria uma sessão com o banco de dados, mantendo a garantia que será fechada.
    Usado como dependencia do FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
