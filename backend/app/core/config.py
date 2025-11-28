import os
from dotenv import load_dotenv

load_dotenv()

# Configurações de segurnaça token
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360
