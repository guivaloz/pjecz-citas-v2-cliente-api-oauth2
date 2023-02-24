"""
Pago de Pensiones Alimenticias - Solicitudes V3, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
import pathlib
from typing import Any
import uuid

from sqlalchemy.orm import Session

from config.settings import UPLOADS_DIR
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_expediente, safe_integer, safe_string

from ...core.cit_clientes.models import CitCliente
from ...core.ppa_solicitudes.models import PpaSolicitud
from ..autoridades.crud import get_autoridad_from_clave
from ..cit_clientes.crud import get_cit_cliente, create_cit_cliente
from .schemas import PpaSolicitudIn, PpaSolicitudOut

CLOUD_STORAGE_URL = "https://noexiste.com"


def get_ppa_solicitudes(db: Session, cit_cliente_id: int) -> Any:
    """Consultar las solicitudes activas"""
    # Consulta
    consulta = db.query(PpaSolicitud)
    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(PpaSolicitud.cit_cliente == cit_cliente)
    # Entregar
    return consulta.filter_by(estatus="A").order_by(PpaSolicitud.id.desc())


def get_ppa_solicitud(db: Session, ppa_solicitud_id: int) -> PpaSolicitud:
    """Consultar una solicitud por su id hasheado"""
    ppa_solicitud = db.query(PpaSolicitud).get(ppa_solicitud_id)
    if ppa_solicitud is None:
        raise CitasNotExistsError("No existe esa solicitud")
    if ppa_solicitud.estatus != "A":
        raise CitasIsDeletedError("No es activa esa solicitud, está eliminada")
    return ppa_solicitud


def get_ppa_solicitud_from_id_hasheado(db: Session, ppa_solicitud_id_hasheado: str) -> PpaSolicitud:
    """Consultar una solicitud por su id hasheado"""
    ppa_solicitud_id = descifrar_id(ppa_solicitud_id_hasheado)
    if ppa_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")
    return get_ppa_solicitud(db, ppa_solicitud_id)


def create_ppa_solicitud(db: Session, datos: PpaSolicitudIn) -> PpaSolicitudOut:
    """Crear una solicitud"""

    # Validar autoridad
    autoridad = get_autoridad_from_clave(db, datos.autoridad_clave)

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

    # Validar compañía telefónica
    compania_telefonica = safe_string(datos.compania_telefonica)
    if compania_telefonica == "":
        raise CitasNotValidParamError("La compañía telefónica no es válida")

    # Validar número de expediente
    numero_expediente = safe_expediente(datos.numero_expediente)
    if numero_expediente == "":
        raise CitasNotValidParamError("El número de expediente no es válido")

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
    ppa_solicitud = PpaSolicitud(
        autoridad=autoridad,
        cit_cliente=cit_cliente,
        domicilio_calle=domicilio_calle,
        domicilio_numero=domicilio_numero,
        domicilio_colonia=domicilio_colonia,
        domicilio_cp=domicilio_cp,
        compania_telefonica=compania_telefonica,
        numero_expediente=numero_expediente,
        identificacion_oficial_archivo="",
        identificacion_oficial_url="",
        comprobante_domicilio_archivo="",
        comprobante_domicilio_url="",
        autorizacion_archivo="",
        autorizacion_url="",
        caducidad=caducidad.date(),
    )
    db.add(ppa_solicitud)
    db.commit()
    db.refresh(ppa_solicitud)

    # Entregar
    return ppa_solicitud


def upload_identificacion_oficial(
    db: Session,
    id_hasheado: str,
    identificacion_oficial: bytes,
) -> PpaSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    ppa_solicitud_id = descifrar_id(id_hasheado)
    if ppa_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")
    ppa_solicitud = get_ppa_solicitud(db, ppa_solicitud_id)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{ppa_solicitud.id:06d}-{uuid.uuid4().hex[:6]}.pdf"

    # Crear el directorio con path si este no existe
    directorio = pathlib.Path(f"{UPLOADS_DIR}/ppa_solicitudes/identificaciones_oficiales")
    directorio.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo
    if UPLOADS_DIR != "":
        with open(f"{directorio}/{archivo}", "wb") as f:
            f.write(identificacion_oficial)

    # Definir el URL
    url = f"{CLOUD_STORAGE_URL}/ppa_solicitudes/identificaciones_oficiales/{archivo}"

    # Actualizar
    ppa_solicitud.identificacion_oficial_archivo = archivo
    ppa_solicitud.identificacion_oficial_url = url
    db.add(ppa_solicitud)
    db.commit()
    db.refresh(ppa_solicitud)

    # Entregar
    return ppa_solicitud


def upload_comprobante_domicilio(
    db: Session,
    id_hasheado: str,
    comprobante_domicilio: bytes,
) -> PpaSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    ppa_solicitud_id = descifrar_id(id_hasheado)
    if ppa_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")
    ppa_solicitud = get_ppa_solicitud(db, ppa_solicitud_id)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{ppa_solicitud.id:06d}-{uuid.uuid4().hex[:6]}.pdf"

    # Crear el directorio con path si este no existe
    directorio = pathlib.Path(f"{UPLOADS_DIR}/ppa_solicitudes/comprobantes_domicilios")
    directorio.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo
    if UPLOADS_DIR != "":
        with open(f"{directorio}/{archivo}", "wb") as f:
            f.write(comprobante_domicilio)

    # Definir el URL
    url = f"{CLOUD_STORAGE_URL}/ppa_solicitudes/comprobantes_domicilios/{archivo}"

    # Actualizar
    ppa_solicitud.comprobante_domicilio_archivo = archivo
    ppa_solicitud.comprobante_domicilio_url = url
    db.add(ppa_solicitud)
    db.commit()
    db.refresh(ppa_solicitud)

    # Entregar
    return ppa_solicitud


def upload_autorizacion(
    db: Session,
    id_hasheado: str,
    autorizacion: bytes,
) -> PpaSolicitudOut:
    """Subir identificación oficial"""

    # Validar ID hasheado
    ppa_solicitud_id = descifrar_id(id_hasheado)
    if ppa_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")
    ppa_solicitud = get_ppa_solicitud(db, ppa_solicitud_id)

    # Definir el nombre del archivo con el ID de seis dígitos y una cadena aleatoria de seis caracteres
    archivo = f"{ppa_solicitud.id:06d}-{uuid.uuid4().hex[:16]}.pdf"

    # Crear el directorio con path si este no existe
    directorio = pathlib.Path(f"{UPLOADS_DIR}/ppa_solicitudes/autorizaciones")
    directorio.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo
    if UPLOADS_DIR != "":
        with open(f"{directorio}/{archivo}", "wb") as f:
            f.write(autorizacion)

    # Definir el URL
    autorizacion_url = f"{CLOUD_STORAGE_URL}/ppa_solicitudes/autorizaciones/{archivo}"

    # Actualizar
    ppa_solicitud.autorizacion_archivo = archivo
    ppa_solicitud.autorizacion_url = autorizacion_url
    db.add(ppa_solicitud)
    db.commit()
    db.refresh(ppa_solicitud)

    # Entregar
    return ppa_solicitud
