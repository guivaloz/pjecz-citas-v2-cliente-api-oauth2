"""
Pagos Tramites y Servicios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string
from .models import PagTramiteServicio


def get_pag_tramites_servicios(db: Session) -> Any:
    """Consultar los tramites y servicios activos"""

    # Consulta
    consulta = db.query(PagTramiteServicio)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(PagTramiteServicio.clave)


def get_pag_tramite_servicio(db: Session, pag_tramite_servicio_id: int) -> PagTramiteServicio:
    """Consultar un tramite y servicio por su id"""
    pag_tramite_servicio = db.query(PagTramiteServicio).get(pag_tramite_servicio_id)
    if pag_tramite_servicio is None:
        raise IndexError("No existe ese tramite y servicio")
    if pag_tramite_servicio.estatus != "A":
        raise IndexError("No es activo ese tramite y servicio, está eliminado")
    return pag_tramite_servicio
