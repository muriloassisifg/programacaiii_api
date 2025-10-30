FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para o PostgreSQL e Pillow
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependências
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install poetry

# Configura Poetry para não criar ambiente virtual (já estamos no container)
RUN poetry config virtualenvs.create false

# Instala as dependências
RUN poetry install --no-dev

# Copia o código da aplicação
COPY ./app /app

# Expõe a porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]