# Usamos una imagen de Python oficial y ligera (compatible con >=3.13 definido en pyproject.toml)
FROM python:3.13-slim

# Configuración para evitar archivos basura de Python y ver los logs al instante
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias esenciales del sistema (requeridas para compilar ciertas librerías de Python/FAISS)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar `uv` de manera global dentro del contenedor
RUN pip install --no-cache-dir uv

# Establecer el directorio de trabajo
WORKDIR /app

# Copiamos primero los archivos de dependencias para aprovechar la caché de Docker
COPY pyproject.toml uv.lock* ./

# Instalamos las dependencias definidas en el pyproject.toml de manera global en el contenedor usando uv.
RUN uv pip install --system --no-cache .

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# Comando para ejecutar tu aplicación de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]