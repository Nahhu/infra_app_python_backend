FROM python:3.12-slim

# Evita archivos pyc y salida bufferizada
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expón el puerto donde Django correrá
EXPOSE 8000

# Ejecuta migraciones y levanta el servidor
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
