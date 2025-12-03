import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega o arquivo .env da raiz do projeto (desenvolvimento local)
# No Docker, as variáveis já vêm do env_file no docker-compose.yml
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = BASE_DIR / ".env"

# Tenta carregar o .env se existir (desenvolvimento local)
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)

# Configurações de segurança token
# As variáveis vêm do .env (local) ou das env vars do Docker
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY não está definida. Verifique o arquivo .env ou as variáveis de ambiente do Docker.")

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360
