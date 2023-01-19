# pjecz-citas-v2-cliente-api-oauth2

API del Sistema de Citas versión 2 del Poder Judicial del Estado de Coahuila de Zaragoza

## Configurar

Genere el `SECRET_KEY` con este comando

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

    # Database
    DB_HOST=127.0.0.1
    DB_NAME=pjecz_citas_v2
    DB_PASS=****************
    DB_USER=adminpjeczcitasv2

    # OAuth2
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ALGORITHM=HS256
    SECRET_KEY=****************************************************************

    # Limite de citas pendientes por cliente
    LIMITE_CITAS_PENDIENTES=30

    # Redis
    REDIS_URL=redis://127.0.0.1
    TASK_QUEUE=pjecz_citas_v2

    # Salt sirve para cifrar el ID con HashID, debe ser igual en Admin
    SALT=********************************

    # Santander Web Pay Plus
    WPP_COMMERCE_ID=XXXXXXXX
    WPP_COMPANY_ID=XXXXXXXX
    WPP_BRANCH_ID=XXXXXXXX
    WPP_KEY=XXXXXXXX
    WPP_PASS=XXXXXXXX
    WPP_TIMEOUT=XXXXXXXX
    WPP_URL=XXXXXXXX
    WPP_USER=XXXXXXXX

    # URLs de las encuestas
    POLL_SERVICE_URL=http://127.0.0.1:3000/poll_service
    POLL_SYSTEM_URL=http://127.0.0.1:3000/poll_system

    # Arrancar con gunicorn o uvicorn
    ARRANCAR=uvicorn

Para Bash Shell cree un archivo `.bashrc` con este contenido

    if [ -f ~/.bashrc ]; then
        source ~/.bashrc
    fi

    source venv/bin/activate
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi

    figlet Citas V2 API OAuth2
    echo

    echo "-- Variables de entorno"
    echo "   ACCESS_TOKEN_EXPIRE_MINUTES: ${ACCESS_TOKEN_EXPIRE_MINUTES}"
    echo "   ALGORITHM: ${ALGORITHM}"
    echo "   DB_HOST: ${DB_HOST}"
    echo "   DB_NAME: ${DB_NAME}"
    echo "   DB_USER: ${DB_USER}"
    echo "   DB_PASS: ${DB_PASS}"
    echo "   LIMITE_CITAS_PENDIENTES: ${LIMITE_CITAS_PENDIENTES}"
    echo "   POLL_SERVICE_URL: ${POLL_SERVICE_URL}"
    echo "   POLL_SYSTEM_URL: ${POLL_SYSTEM_URL}"
    echo "   REDIS_URL: ${REDIS_URL}"
    echo "   SALT: ${SALT}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo "   TASK_QUEUE: ${TASK_QUEUE}"
    echo "   WPP_COMMERCE_ID: ${WPP_COMMERCE_ID}"
    echo "   WPP_COMPANY_ID: ${WPP_COMPANY_ID}"
    echo "   WPP_BRANCH_ID: ${WPP_BRANCH_ID}"
    echo "   WPP_KEY: ${WPP_KEY}"
    echo "   WPP_PASS: ${WPP_PASS}"
    echo "   WPP_TIMEOUT: ${WPP_TIMEOUT}"
    echo "   WPP_URL: ${WPP_URL}"
    echo "   WPP_USER: ${WPP_USER}"
    echo

    export PGDATABASE=${DB_NAME}
    export PGPASSWORD=${DB_PASS}
    export PGUSER=${DB_USER}
    echo "-- PostgreSQL"
    echo "   PGDATABASE: ${PGDATABASE}"
    echo "   PGPASSWORD: ${PGPASSWORD}"
    echo "   PGUSER:     ${PGUSER}"
    echo

    alias arrancar="uvicorn --host 0.0.0.0 --port 8005 --reload citas_cliente.app:app"
    echo "-- FastAPI"
    echo "   arrancar"
    echo

Cree el archivo `instance/settings.py` que cargue las variables de entorno

    """
    Configuración para desarrollo
    """
    import os


    # Base de datos
    DB_USER = os.environ.get("DB_USER", "wronguser")
    DB_PASS = os.environ.get("DB_PASS", "badpassword")
    DB_NAME = os.environ.get("DB_NAME", "pjecz_citas_v2")
    DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")

    # MariaDB o MySQL
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # PostgreSQL
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    # SQLite
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///pjecz_citas_v2.sqlite3'

    # CORS or "Cross-Origin Resource Sharing" refers to the situations when a frontend
    # running in a browser has JavaScript code that communicates with a backend,
    # and the backend is in a different "origin" than the frontend.
    # https://fastapi.tiangolo.com/tutorial/cors/
    ORIGINS = [
        "http://localhost:8005",
        "http://localhost:3000",
        "http://127.0.0.1:8005",
        "http://127.0.0.1:3000",
    ]

## Crear Entorno Virtual

Crear el enorno virtual dentro de la copia local del repositorio, con

    python -m venv venv

O con virtualenv

    virtualenv -p python3 venv

Active el entorno virtual, en Linux con...

    source venv/bin/activate

O en windows con

    venv/Scripts/activate

Verifique que haya el mínimo de paquetes con

    pip list

Actualice el pip de ser necesario

    pip install --upgrade pip

Y luego instale los paquetes requeridos

    pip install -r requirements.txt

Verifique con

    pip list

## FastAPI

Arrancar con uvicorn

    uvicorn --host=0.0.0.0 --port 8005 --reload citas_cliente.app:app

O arrancar con gunicorn

    gunicorn -w 4 -k uvicorn.workers.UvicornWorker citas_cliente.app:app
