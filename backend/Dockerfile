# Estágio de build para reduzir o tamanho final
FROM python:3.12-alpine AS builder

WORKDIR /app

# Instalar dependências necessárias para compilar pacotes se necessário
RUN apk add --no-cache gcc musl-dev mariadb-connector-c-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Estágio final
FROM python:3.12-alpine

WORKDIR /app

# Instalar dependências de runtime do MariaDB/MySQL
RUN apk add --no-cache mariadb-connector-c tzdata

# Definir a variável de ambiente para o fuso horário desejado
ENV TZ=America/Recife

# Copiar apenas as bibliotecas instaladas
COPY --from=builder /install /usr/local

# Copiar o código da aplicação
COPY . .

# Criar um usuário não-root para segurança
RUN chmod +x entrypoint.sh \
    && adduser -D appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expor a porta que o FastAPI utiliza
EXPOSE 8000

# Aplica migrações SQLAlchemy e inicia a API
ENTRYPOINT ["./entrypoint.sh"]
