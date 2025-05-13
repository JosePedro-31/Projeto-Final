FROM python:3.11-buster

# Atualiza o sistema e instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 libsqlite3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos do projeto
COPY app /app
COPY data /app/data
COPY requirements.txt /app/requirements.txt

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do Python
RUN pip install -r requirements.txt

# Comando para executar a aplicação
CMD ["python", "main.py"]