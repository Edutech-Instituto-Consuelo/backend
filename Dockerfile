# Imagem base (utilizando Python 3.10 slim) - uma imagem leve para reduzir o tamanho do contêiner
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container. Tudo o que o Docker fizer depois daqui será dentro de /app
WORKDIR /app

# Configurações básicas do Python
# - Não gerar arquivos .pyc (cache)
# - Logs sem buffer (debug mais fácil)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Instala dependências do sistema operacional. Necessário para instalar bibliotecas Python que dependem de compilação
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências Python listadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do diretório atual para o diretório de trabalho dentro do container
COPY . .

# Comando para iniciar a aplicação usando Uvicorn, especificando o módulo e a aplicação FastAPI, além do host e porta
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]