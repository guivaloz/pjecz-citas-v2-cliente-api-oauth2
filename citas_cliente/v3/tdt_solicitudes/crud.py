"""
Tres de Tres - Solicitudes V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_integer, safe_string, safe_url

from ...core.cit_clientes.models import CitCliente
from ...core.tdt_solicitudes.models import TdtSolicitud
from ..cit_clientes.crud import get_cit_cliente, create_cit_cliente
from ..municipios.crud import get_municipio_from_id_hasheado
from ..tdt_partidos.crud import get_tdt_partido_from_siglas
from .schemas import TdtSolicitudIn, TdtSolicitudOut


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
        raise CitasNotExistsError("El ID de la solicitud no es válida")
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

    # Validar identificación oficial archivo
    identificacion_oficial_archivo = safe_string(datos.identificacion_oficial_archivo, do_unidecode=False, to_uppercase=False)
    if identificacion_oficial_archivo == "":
        raise CitasNotValidParamError("El archivo de la identificación oficial no es válido")

    # Validar identificación oficial URL
    identificacion_oficial_url = safe_url(datos.identificacion_oficial_url)
    if identificacion_oficial_url == "":
        raise CitasNotValidParamError("El URL de la identificación oficial no es válido")

    # Validar comprobante de domicilio archivo
    comprobante_domicilio_archivo = safe_string(datos.comprobante_domicilio_archivo, do_unidecode=False, to_uppercase=False)
    if comprobante_domicilio_archivo == "":
        raise CitasNotValidParamError("El archivo del comprobante de domicilio no es válido")

    # Validar comprobante de domicilio URL
    comprobante_domicilio_url = safe_url(datos.comprobante_domicilio_url)
    if comprobante_domicilio_url == "":
        raise CitasNotValidParamError("El URL del comprobante de domicilio no es válido")

    # Validar autorización archivo
    autorizacion_archivo = safe_string(datos.autorizacion_archivo, do_unidecode=False, to_uppercase=False)
    if autorizacion_archivo == "":
        raise CitasNotValidParamError("El archivo de la autorización no es válido")

    # Validar autorización URL
    autorizacion_url = safe_url(datos.autorizacion_url)
    if autorizacion_url == "":
        raise CitasNotValidParamError("El URL de la autorización no es válido")

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
        identificacion_oficial_archivo=identificacion_oficial_archivo,
        identificacion_oficial_url=identificacion_oficial_url,
        comprobante_domicilio_archivo=comprobante_domicilio_archivo,
        comprobante_domicilio_url=comprobante_domicilio_url,
        autorizacion_archivo=autorizacion_archivo,
        autorizacion_url=autorizacion_url,
    )
    db.add(tdt_solicitud)
    db.commit()
    db.refresh(tdt_solicitud)

    # Entregar
    return tdt_solicitud
