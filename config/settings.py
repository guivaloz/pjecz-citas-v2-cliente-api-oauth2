"""
Configuración para producción
"""
import os
import pytz

# Google Cloud SQL
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "pjecz_citas_v2")
DB_PASS = os.environ.get("DB_PASS", "wrongpassword")
DB_USER = os.environ.get("DB_USER", "nouser")

# Google Cloud SQL a Minerva con PostgreSQL
SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Always in False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# OAuth2
SECRET_KEY = os.environ.get("SECRET_KEY")  # openssl rand -hex 32
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend
# running in a browser has JavaScript code that communicates with a backend,
# and the backend is in a different "origin" than the frontend.
# https://fastapi.tiangolo.com/tutorial/cors/
ORIGINS = os.environ.get("ORIGINS", "http://localhost:5000,http://127.0.0.1:5000").split(",")

# Husos horarios
LOCAL_HUSO_HORARIO = pytz.timezone(os.environ.get("LOCAL_HUSO_HORARIO", "America/Mexico_City"))
if os.environ.get("SERVIDOR_HUSO_HORARIO"):
    SERVIDOR_HUSO_HORARIO = pytz.timezone(os.environ.get("SERVIDOR_HUSO_HORARIO"))
else:
    SERVIDOR_HUSO_HORARIO = pytz.utc

# Limite de citas pendientes por cliente
LIMITE_CITAS_PENDIENTES = int(os.environ.get("LIMITE_CITAS_PENDIENTES", "0"))

# Redis
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1")
TASK_QUEUE = os.environ.get("TASK_QUEUE", "pjecz_citas_v2")

# Salt sirve para cifrar el ID con HashID, debe ser igual en Admin
SALT = os.environ.get("SALT", "Esta es una muy mala cadena aleatoria")

# URLs de las encuestas
POLL_SERVICE_URL = os.environ.get("POLL_SERVICE_URL", "")
POLL_SYSTEM_URL = os.environ.get("POLL_SYSTEM_URL", "")

# Directorio donde se guardan los archivos subidos
UPLOADS_DIR = os.environ.get("UPLOADS_DIR", "")
