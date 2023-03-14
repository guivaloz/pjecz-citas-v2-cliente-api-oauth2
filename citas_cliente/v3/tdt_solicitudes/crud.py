"""
Tres de Tres - Solicitudes V3, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import uuid

from dotenv import load_dotenv
from google.cloud import storage
from sqlalchemy.orm import Session

from config.settings import CLOUD_STORAGE_DEPOSITO
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_integer, safe_string

from ...core.cit_clientes.models import CitCliente
from ...core.tdt_solicitudes.models import TdtSolicitud
from ..cit_clientes.crud import get_cit_cliente, create_cit_cliente
from ..municipios.crud import get_municipio_from_id_hasheado
from ..tdt_partidos.crud import get_tdt_partido_from_siglas
from .schemas import TdtSolicitudIn, TdtSolicitudOut

load_dotenv()  # Take environment variables from .env

SUBDIRECTORIO = "tres-de-tres"


def get_tdt_solicitudes(db: Session, cit_cliente_id: int) -> Any:
    """Consultar las solicitudes activos"""
    # Consultar
    consulta = db.query(TdtSolicitud)
    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(TdtSolicitud.cit_cliente == cit_cliente)
    # Entregar
    return consulta.filter_by(estatus="A").order_by(TdtSolicitud.id.desc())


def get_tdt_solicitud(db: Session, tdt_solicitud_id: int) -> TdtSolicitud:
    """Consultar una solicitud por su id hasheado"""
    tdt_solicitud = db.query(TdtSolicitud).get(tdt_solicitud_id)
    if tdt_solicitud is None:
        raise CitasNotExistsError("No existe esa solicitud")
    if tdt_solicitud.estatus != "A":
        raise CitasIsDeletedError("No es activa esa solicitud, está eliminada")
    return tdt_solicitud


def get_tdt_solicitud_from_id_hasheado(db: Session, tdt_solicitud_id_hasheado: str) -> TdtSolicitud:
    """Consultar un solicitud por su id hasheado"""
    tdt_solicitud_id = descifrar_id(tdt_solicitud_id_hasheado)
    if tdt_solicitud_id is None:
        raise CitasNotValidParamError("El ID de la solicitud no es válida")
    return get_tdt_solicitud(db, tdt_solicitud_id)


def create_tdt_solicitud(
    db: Session,
    datos: TdtSolicitudIn,
) -> TdtSolicitudOut:
    """Crear una solicitud"""

    # Validar municipio
    municipio = get_municipio_from_id_hasheado(db, datos.municipio_id_hasheado)

    # Validar partido
    tdt_partido = get_tdt_partido_from_siglas(db, datos.tdt_partido_siglas)

    # Validar cargo
    cargo = safe_string(datos.cargo)
    if cargo not in TdtSolicitud.CARGOS:
        raise CitasNotValidParamError("El cargo no es válido")

    # Validar principio
    principio = safe_string(datos.principio)
    if principio not in TdtSolicitud.PRINCIPIOS:
        raise CitasNotValidParamError("El principio no es válido")

    # Validar domicilio calle
    domicilio_calle = safe_string(datos.domicilio_calle, save_enie=True)
    if domicilio_calle == "":
        raise CitasNotValidParamError("La calle del domicilio no es válida")

    # Validar domicilio número
    domicilio_numero = safe_string(datos.domicilio_numero)
    if domicilio_numero == "":
        raise CitasNotValidParamError("El número del domicilio no es válido")

    # Validar domicilio colonia
    domicilio_colonia = safe_string(datos.domicilio_colonia, save_enie=True)
    if domicilio_colonia == "":
        raise CitasNotValidParamError("La colonia del domicilio no es válida")

    # Validar domicilio CP
    domicilio_cp = safe_integer(datos.domicilio_cp, default=0)
    if domicilio_cp == 0:
        raise CitasNotValidParamError("El código postal del domicilio no es válido")

    # Validar y crear cliente de no existir
    cit_cliente = create_cit_cliente(
        db,
        CitCliente(
            nombres=datos.cit_cliente_nombres,
            apellido_primero=datos.cit_cliente_apellido_primero,
            apellido_segundo=datos.cit_cliente_apellido_segundo,
            curp=datos.cit_cliente_curp,
            email=datos.cit_cliente_email,
            telefono=datos.cit_cliente_telefono,
        ),
    )

    # Definir la fecha de caducidad que sea dentro de 30 días
    caducidad = datetime.now() + timedelta(days=30)

    # Crear solicitud
    tdt_solicitud = TdtSolicitud(
        cit_cliente=cit_cliente,
        municipio=municipio,
        tdt_partido=tdt_partido,
        cargo=cargo,
        principio=principio,
        domicilio_calle=domicilio_calle,
        domicilio_numero=domicilio_numero,
        domicilio_colonia=domicilio_colonia,
        domicilio_cp=domicilio_cp,
        identificacion_oficial_archivo="",
        identificacion_oficial_url="",
        comprobante_domicilio_archivo="",
        comprobante_domicilio_url="",
        autorizacion_archivo="",
        autorizacion_url="",
        caducidad=caducidad.date(),
    )
    db.add(tdt_solicitud)
    db.commit()
    db.refresh(tdt_solicitud)

    # Entregar
    return tdt_solicitud


def upload_identificacion_oficial(
    db: Session,
    id_hasheado: str,
    identificacion_oficial: bytes,
) -> TdtSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    tdt_solicitud_id = descifrar_id(id_hasheado)
    if tdt_solicitud_id is None:
        raise CitasNotValidParamError("El ID de la solicitud no es válida")
    tdt_solicitud = get_tdt_solicitud(db, tdt_solicitud_id)

    # Definir el directorio
    upload_date = datetime.now()
    year_str = upload_date.strftime("%Y")
    month_str = upload_date.strftime("%m")
    directorio = Path(SUBDIRECTORIO, year_str, month_str)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{tdt_solicitud.id:06d}-identificacion-oficial-{uuid.uuid4().hex[:16]}.pdf"

    # Definir la ruta
    ruta = Path(directorio, archivo)

    # Si no se ha definido CLOUD_STORAGE_DEPOSITO, se guarda si existe el directorio
    if CLOUD_STORAGE_DEPOSITO == "":
        if not directorio.exists():
            with open(ruta, "wb") as puntero:
                puntero.write(identificacion_oficial)
        url = f"http://noexiste.com/{str(ruta)}"

    # Subir el archivo a Google Storage
    if CLOUD_STORAGE_DEPOSITO != "":
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_STORAGE_DEPOSITO)
        blob = bucket.blob(str(ruta))
        blob.upload_from_string(identificacion_oficial, content_type="application/pdf")
        url = blob.public_url

    # Actualizar
    tdt_solicitud.identificacion_oficial_archivo = archivo
    tdt_solicitud.identificacion_oficial_url = url
    db.add(tdt_solicitud)
    db.commit()
    db.refresh(tdt_solicitud)

    # Entregar
    return tdt_solicitud


def upload_comprobante_domicilio(
    db: Session,
    id_hasheado: str,
    comprobante_domicilio: bytes,
) -> TdtSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    tdt_solicitud_id = descifrar_id(id_hasheado)
    if tdt_solicitud_id is None:
        raise CitasNotValidParamError("El ID de la solicitud no es válida")
    tdt_solicitud = get_tdt_solicitud(db, tdt_solicitud_id)

    # Definir el directorio
    upload_date = datetime.now()
    year_str = upload_date.strftime("%Y")
    month_str = upload_date.strftime("%m")
    directorio = Path(SUBDIRECTORIO, year_str, month_str)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{tdt_solicitud.id:06d}-comprobante-domicilio-{uuid.uuid4().hex[:16]}.pdf"

    # Definir la ruta
    ruta = Path(directorio, archivo)

    # Si no se ha definido CLOUD_STORAGE_DEPOSITO, se guarda si existe el directorio
    if CLOUD_STORAGE_DEPOSITO == "":
        if not directorio.exists():
            with open(ruta, "wb") as puntero:
                puntero.write(comprobante_domicilio)
        url = f"http://noexiste.com/{str(ruta)}"

    # Subir el archivo a Google Storage
    if CLOUD_STORAGE_DEPOSITO != "":
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_STORAGE_DEPOSITO)
        blob = bucket.blob(str(ruta))
        blob.upload_from_string(comprobante_domicilio, content_type="application/pdf")
        url = blob.public_url

    # Actualizar
    tdt_solicitud.comprobante_domicilio_archivo = archivo
    tdt_solicitud.comprobante_domicilio_url = url
    db.add(tdt_solicitud)
    db.commit()
    db.refresh(tdt_solicitud)

    # Entregar
    return tdt_solicitud


def upload_autorizacion(
    db: Session,
    id_hasheado: str,
    autorizacion: bytes,
) -> TdtSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    tdt_solicitud_id = descifrar_id(id_hasheado)
    if tdt_solicitud_id is None:
        raise CitasNotValidParamError("El ID de la solicitud no es válida")
    tdt_solicitud = get_tdt_solicitud(db, tdt_solicitud_id)

    # Definir el directorio
    upload_date = datetime.now()
    year_str = upload_date.strftime("%Y")
    month_str = upload_date.strftime("%m")
    directorio = Path(SUBDIRECTORIO, year_str, month_str)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{tdt_solicitud.id:06d}-autorizacion-{uuid.uuid4().hex[:16]}.pdf"

    # Definir la ruta
    ruta = Path(directorio, archivo)

    # Si no se ha definido CLOUD_STORAGE_DEPOSITO, se guarda si existe el directorio
    if CLOUD_STORAGE_DEPOSITO == "":
        if not directorio.exists():
            with open(ruta, "wb") as puntero:
                puntero.write(autorizacion)
        url = f"http://noexiste.com/{str(ruta)}"

    # Subir el archivo a Google Storage
    if CLOUD_STORAGE_DEPOSITO != "":
        storage_client = storage.Client()
        bucket = storage_client.bucket(CLOUD_STORAGE_DEPOSITO)
        blob = bucket.blob(str(ruta))
        blob.upload_from_string(autorizacion, content_type="application/pdf")
        url = blob.public_url

    # Actualizar
    tdt_solicitud.autorizacion_archivo = archivo
    tdt_solicitud.autorizacion_url = url
    db.add(tdt_solicitud)
    db.commit()
    db.refresh(tdt_solicitud)

    # Entregar
    return tdt_solicitud
