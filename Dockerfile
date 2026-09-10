# Imagem base enxuta com Python 3.14.
FROM python:3.14-slim

# Diretório de trabalho da aplicação dentro do container.
WORKDIR /app

# Instala as dependências antes de copiar o restante do projeto,
# permitindo melhor aproveitamento do cache de camadas do Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código e os arquivos estáticos da aplicação.
COPY . .

# O Cloud Run fornece a variável PORT.
# Para execução local, a aplicação utiliza 8000 como fallback.
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
