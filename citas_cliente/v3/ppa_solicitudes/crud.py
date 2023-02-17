"""
Pago de Pensiones Alimenticias - Solicitudes V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from config.settings import LIMITE_CITAS_PENDIENTES
from lib.exceptions import CitasAnyError, CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_curp, safe_email, safe_integer, safe_string, safe_telefono

from ...core.cit_clientes.models import CitCliente
from ...core.ppa_solicitudes.models import PpaSolicitud
from ..autoridades.crud import get_autoridad_from_clave
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_from_curp, get_cit_cliente_from_email


def get_ppa_solicitudes(
    db: Session,
    cit_cliente_id: int,
) -> Any:
    """Consultar las solicitudes activas"""

    # Consulta
    consulta = db.query(PpaSolicitud)

    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(PpaSolicitud.cit_cliente == cit_cliente)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(PpaSolicitud.id)


def get_ppa_solicitud(
    db: Session,
    ppa_solicitud_id_haseado: str,
) -> PpaSolicitud:
    """Consultar una solicitud por su id hasheado"""

    # Descrifrar el ID hasheado
    ppa_solicitud_id = descifrar_id(ppa_solicitud_id_haseado)
    if ppa_solicitud_id is None:
        raise CitasNotExistsError("El ID de la solicitud no es válida")

    # Consultar
    ppa_solicitud = db.query(PpaSolicitud).get(ppa_solicitud_id)

    # Validar
    if ppa_solicitud is None:
        raise CitasNotExistsError("No existe ese solicitud")
    if ppa_solicitud.estatus != "A":
        raise CitasIsDeletedError("No es activo ese solicitud, está eliminado")

    # Entregar
    return ppa_solicitud
