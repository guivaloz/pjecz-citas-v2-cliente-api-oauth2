"""
Tres de Tres - Solicitudes V3, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from config.settings import LOCAL_HUSO_HORARIO, LIMITE_CITAS_PENDIENTES
from lib.exceptions import CitasAnyError, CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_curp, safe_email, safe_integer, safe_string, safe_telefono

from ...core.cit_clientes.models import CitCliente
from ...core.tdt_solicitudes.models import TdtSolicitud
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_from_curp, get_cit_cliente_from_email
from ..municipios.crud import get_municipio


def get_tdt_solicitudes(
    db: Session,
    cit_cliente_id: int,
) -> Any:
    """Consultar las solicitudes activos"""

    # Consultar
    consulta = db.query(TdtSolicitud)

    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(TdtSolicitud.cit_cliente == cit_cliente)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(TdtSolicitud.id)


def get_tdt_solicitud(
    db: Session,
    tdt_solicitud_id_hasheado: str,
) -> TdtSolicitud:
    """Consultar una solicitud por su id hasheado"""

    # Descrifrar el ID hasheado
    tdt_solicitud_id = descifrar_id(tdt_solicitud_id_hasheado)
    if tdt_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")

    # Consultar
    tdt_solicitud = db.query(TdtSolicitud).get(tdt_solicitud_id)

    # Validar
    if tdt_solicitud is None:
        raise CitasNotExistsError("No existe ese solicitud")
    if tdt_solicitud.estatus != "A":
        raise CitasIsDeletedError("No es activo ese solicitud, está eliminado")

    # Entregar
    return tdt_solicitud
