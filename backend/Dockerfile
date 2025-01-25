FROM python:3.11-slim

# Instalace SQLite CLI
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Nastavení pracovního adresáře
WORKDIR /app

# Zkopíruj požadavky a nainstaluj je
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Zkopíruj aplikaci
COPY . .

# Expozice portu a spuštění serveru
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
