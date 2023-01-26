# pjecz-citas-v2-cliente-api-oauth2

API del Sistema de Citas versión 2 del Poder Judicial del Estado de Coahuila de Zaragoza

## Mejores prácticas

En la versión 3 usa las recomendaciones de [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/) que recomienda entregar un _status code_ **200** y un _body_ con el atributo `success` que indique si la operación fue exitosa o no, asi como un `message` donde explique el error.

### Respuesta exitosa

Status code: **200**

Body que entrega un listado

    {
        "success": true,
        "message": "Success",
        "result": {
            "total": 2812,
            "items": [ { "id": 1, ... } ],
            "limit": 100,
            "offset": 0
        }
    }

Body que entrega un item

    {
        "success": true,
        "message": "Success",
        "id": 123,
        ...
    }

### Respuesta fallida: registro no encontrado

Status code: **200**

Body

    {
        "success": false,
        "message": "No employee found for ID 100"
    }

## Configurar

Genere el `SECRET_KEY` con este comando

    openssl rand -hex 32

Cree un archivo para las variables de entorno `.env`

    # CORS Origins separados por comas
    ORIGINS=http://localhost:8005,http://127.0.0.1:8005

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
    WPP_COMPANY_ID=XXXX
    WPP_BRANCH_ID=NNNN
    WPP_KEY=XXXXXXXX
    WPP_PASS=XXXXXXXX
    WPP_TIMEOUT=12
    WPP_URL=https://noexiste.com
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

    source .venv/bin/activate
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

## Instalar

Crear entorno virtual con Python 3.10

    python3.10 -m venv .venv

Activar entorno virtual

    source .venv/bin/activate

Actualizar pip de ser necesario

    pip install --upgrade pip

Instalar Poetry de ser necesario

    pip install poetry

Instalar dependencias

    poetry install

## Configure Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

    poetry config --list
    poetry config virtualenvs.in-project true

Verifique que este en True

    poetry config virtualenvs.in-project

## Google Cloud deployment

Crear el archivo `app.yaml` con las variables para producción

    runtime: python310
    instance_class: F2
    service: citas-api-oauth2
    entrypoint: gunicorn -w 4 -k uvicorn.workers.UvicornWorker citas_cliente.app:app
    env_variables:
      ACCESS_TOKEN_EXPIRE_MINUTES: 30
      ALGORITHM: HS256
      CLOUD_SQL_CONNECTION_NAME: justicia-digital-gob-mx:us-west2:minerva
      DB_HOST: NNN.NNN.NNN.NNN
      DB_NAME: pjecz_citas_v2
      DB_PASS: XXXXXXXXXXXXXXXX
      DB_USER: adminpjeczcitasv2
      LIMITE_CITAS_PENDIENTES: 30
      ORIGINS: "https://citas.justiciadigital.gob.mx,https://pagos.justiciadigital.gob.mx"
      POLL_SYSTEM_URL: "https://citas.justiciadigital.gob.mx/poll_system"
      POLL_SERVICE_URL: "https://citas.justiciadigital.gob.mx/poll_service"
      REDIS_URL: redis://NNN.NNN.NNN.NNN
      SALT: XXXXXXXXXXXXXXXX
      SECRET_KEY: XXXXXXXXXXXXXXXX
      TASK_QUEUE: pjecz_citas_v2
      WPP_COMMERCE_ID: "XXXXXXXXXXXXXXXX"
      WPP_COMPANY_ID: XXXX
      WPP_BRANCH_ID: "NNNN"
      WPP_KEY: XXXXXXXXXXXXXXXX
      WPP_PASS: XXXXXXXXXXXXXXXX
      WPP_TIMEOUT: 24
      WPP_URL: "https://noexiste.com"
      WPP_USER: XXXXXXXXXXXXXXXX
    vpc_access_connector:
      name: projects/justicia-digital-gob-mx/locations/us-west2/connectors/cupido

Crear el archivo `requirements.txt`

    poetry export -f requirements.txt --output requirements.txt --without-hashes

Y subir a Google Cloud con

    gcloud app deploy
