# Usar uma imagem Python oficial como base
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Instalar dependências para textract e outras bibliotecas
RUN apt-get update && apt-get install -y \
    build-essential \
    libpoppler-cpp-dev \
    pkg-config \
    python3-dev \
    tesseract-ocr \
    libtesseract-dev \
    antiword \
    unrtf \
    poppler-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar os ficheiros de requisitos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código da aplicação
COPY ./app /app

# Definir o volume para os dados
VOLUME ["/app/data"]

# Comando para executar a aplicação
CMD ["python", "main.py"]