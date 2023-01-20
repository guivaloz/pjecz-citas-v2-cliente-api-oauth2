"""
Pagos Tramites y Servicios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_clave

from ...core.pag_tramites_servicios.models import PagTramiteServicio


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


def get_pag_tramite_servicio_from_clave(db: Session, clave: str) -> PagTramiteServicio:
    """Consultar un cliente por su clave"""
    clave = safe_clave(clave)
    if clave == "":
        raise ValueError("No se recibio la clave del tramite o servicio")
    pag_tramite_servicio = db.query(PagTramiteServicio).filter_by(clave=clave).first()
    if pag_tramite_servicio is None:
        raise IndexError("No existe el tramite o servicio")
    if pag_tramite_servicio.estatus != "A":
        raise IndexError("No es activo el tramite o servicio, está eliminado")
    return pag_tramite_servicio
