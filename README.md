# Aplicación Flask Contenerizada con Docker y GitHub Actions

## 📋 Descripción del Proyecto

Este proyecto demuestra cómo contenerizar una aplicación Flask utilizando Docker y automatizar su despliegue en Docker Hub mediante un pipeline de CI/CD con GitHub Actions.

### 🎯 Características

- **Aplicación Flask Simple**: Una API REST básica con múltiples endpoints
- **Contenerización con Docker**: Imagen optimizada basada en Python 3.11-slim
- **Pruebas Automatizadas**: Suite de tests con pytest ejecutadas en el contenedor
- **Pipeline CI/CD**: Automatización completa con GitHub Actions
  - ✅ Build de la imagen Docker
  - ✅ Ejecución de pruebas
  - ✅ Push automático a Docker Hub
- **Documentación Completa**: Instrucciones detalladas para desarrollo y deployment

## 📦 Requisitos Previos

Para trabajar con este proyecto necesitas tener instalado:

- **Docker** 20.10+ ([Instalar Docker Desktop](https://www.docker.com/products/docker-desktop))
- **Docker Compose** (incluido con Docker Desktop)
- **Git** 2.30+
- **Python 3.11+** (solo si ejecutas localmente sin Docker)

## 🚀 Inicio Rápido con Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/flask-docker-app.git
cd flask-docker-app
```

### 2. Construir la imagen Docker

```bash
docker build -t flask-app:latest .
```

### 3. Ejecutar el contenedor

```bash
docker run -p 5000:5000 flask-app:latest
```

La aplicación estará disponible en `http://localhost:5000`

### 4. Verificar que funciona

```bash
# Ruta raíz
curl http://localhost:5000/

# Ruta de información
curl http://localhost:5000/api/info

# Health check
curl http://localhost:5000/health
```

## 🧪 Ejecutar las Pruebas

### En el contenedor

```bash
# Construir imagen
docker build -t flask-app:test .

# Ejecutar pytest
docker run --rm flask-app:test pytest test_app.py -v
```

### Localmente (sin Docker)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest test_app.py -v
```

## 🔑 Configurar Secretos en GitHub

Para que el pipeline pueda hacer push a Docker Hub, necesitas configurar dos secretos en tu repositorio:

### 1. Ir a la configuración del repositorio

- En GitHub, ve a **Settings** → **Secrets and variables** → **Actions**

### 2. Crear `DOCKERHUB_USERNAME`

- Click en **New repository secret**
- **Name**: `DOCKERHUB_USERNAME`
- **Value**: Tu nombre de usuario en Docker Hub
- Click en **Add secret**

### 3. Crear `DOCKERHUB_TOKEN`

- Click en **New repository secret**
- **Name**: `DOCKERHUB_TOKEN`
- **Value**: Tu token de acceso en Docker Hub

Para generar el token en Docker Hub:
1. Inicia sesión en [Docker Hub](https://hub.docker.com)
2. Ve a **Account Settings** → **Security**
3. Click en **New Access Token**
4. Dale un nombre descriptivo
5. Copia el token y pégalo en GitHub

### ✅ Verificar la configuración

Una vez configurados los secretos, el pipeline automáticamente:
- Construirá la imagen
- Ejecutará los tests
- Hará push a Docker Hub en cada push a `main`

## 📁 Estructura del Proyecto

```
flask-docker-app/
├── app.py                          # Aplicación Flask principal
├── test_app.py                     # Suite de tests con pytest
├── requirements.txt                # Dependencias de Python
├── Dockerfile                      # Configuración de Docker
├── README.md                       # Este archivo
└── .github/
    └── workflows/
        └── ci.yml                  # Pipeline de GitHub Actions
```

## 🔄 Descripción del Pipeline CI/CD

### Etapa 1: Build

- **Trigger**: Push o Pull Request a `main`
- **Acciones**:
  - Checkout del código
  - Configuración de Docker Buildx
  - Construcción de la imagen Docker
  - Almacenamiento en caché para builds futuros

### Etapa 2: Test

- **Dependencia**: Requiere que Build sea exitoso
- **Acciones**:
  - Reconstruye la imagen Docker
  - Instala pytest y pytest-cov dentro del contenedor
  - Ejecuta la suite de tests
  - Genera reporte de cobertura de código

### Etapa 3: Push

- **Trigger**: Solo en push a `main` (no en PRs)
- **Dependencia**: Requiere que Test sea exitoso
- **Acciones**:
  - Login a Docker Hub con credenciales seguras
  - Build y push de la imagen con dos tags:
    - `username/flask-app:sha-del-commit` (versión específica)
    - `username/flask-app:latest` (última versión)
  - Utiliza caché de registry para acelerar builds futuros

## 🔗 Endpoints de la Aplicación

### GET `/`

Ruta raíz que responde con un mensaje de saludo.

```bash
curl http://localhost:5000/
```

**Respuesta**:
```json
{
  "message": "¡Hola desde Flask en Docker!",
  "status": "success"
}
```

### GET `/api/info`

Proporciona información sobre la aplicación.

```bash
curl http://localhost:5000/api/info
```

**Respuesta**:
```json
{
  "app_name": "Flask Docker Application",
  "version": "1.0.0",
  "environment": "containerized"
}
```

### GET `/health`

Health check para verificar que la aplicación funciona correctamente.

```bash
curl http://localhost:5000/health
```

**Respuesta**:
```json
{
  "status": "healthy",
  "message": "La aplicación está funcionando correctamente"
}
```

## 🛑 Solución de Problemas

### El contenedor no inicia

```bash
# Ver logs del contenedor
docker logs <container-id>

# Ejecutar en modo interactivo para debug
docker run -it flask-app:latest /bin/bash
```

### Los tests fallan en el contenedor

```bash
# Ejecutar tests con output detallado
docker run --rm flask-app:test pytest test_app.py -vv --tb=short
```

### El push a Docker Hub falla en GitHub Actions

- ✅ Verificar que los secretos `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN` están configurados
- ✅ Verificar que el token no ha expirado
- ✅ Asegurarse que la rama es `main` (el push solo ocurre en `main`)

## 🔐 Buenas Prácticas de Seguridad

1. **Secretos en GitHub**: Nunca commits credenciales en el repositorio
2. **Imagen slim**: Se usa `python:3.11-slim` para reducir superficie de ataque
3. **Cache de registry**: Se utiliza caché de Docker registry para ahorrar ancho de banda
4. **Layer caching**: Dockerfile optimizado para aprovechar caché de capas
5. **Variables de entorno**: `PYTHONUNBUFFERED=1` para mejor logging en contenedores

## 📚 Recursos Útiles

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Documentación oficial de Docker](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Hub](https://hub.docker.com/)
- [Pytest Documentation](https://docs.pytest.org/)

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para sugerencias y mejoras.

---

**Última actualización**: 1 de marzo de 2026
