FROM python:3.8-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    firefox-esr \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Configurar entorno
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

# Comando por defecto
CMD ["pytest", "--browser=firefox", "--headless"]