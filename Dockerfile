# Usar imagen base oficial de Python slim para reducir tamaño
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY app.py .

# Exponer el puerto 5000 (puerto estándar para Flask)
EXPOSE 5000

# Establecer variables de entorno para Flask
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación Flask
# Se ejecuta gunicorn en lugar de flask run para mayor estabilidad en producción
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
