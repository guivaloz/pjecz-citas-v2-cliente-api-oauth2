"""
Pagos Tramites y Servicios V3, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.safe_string import safe_clave

from ...core.pag_tramites_servicios.models import PagTramiteServicio


def get_pag_tramites_servicios(db: Session) -> Any:
    """Consultar los tramites y servicios activos"""
    return db.query(PagTramiteServicio).filter_by(estatus="A").order_by(PagTramiteServicio.id)


def get_pag_tramite_servicio(db: Session, pag_tramite_servicio_id: int) -> PagTramiteServicio:
    """Consultar un tramite y servicio por su id"""
    pag_tramite_servicio = db.query(PagTramiteServicio).get(pag_tramite_servicio_id)
    if pag_tramite_servicio is None:
        raise CitasNotExistsError("No existe ese tramite y servicio")
    if pag_tramite_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese tramite y servicio, está eliminado")
    return pag_tramite_servicio


def get_pag_tramite_servicio_from_clave(db: Session, clave: str) -> PagTramiteServicio:
    """Consultar un cliente por su clave"""
    try:
        clave = safe_clave(clave)
    except ValueError as error:
        raise ValueError("Es incorrecta la clave del tramite o servicio") from error
    pag_tramite_servicio = db.query(PagTramiteServicio).filter_by(clave=clave).first()
    if pag_tramite_servicio is None:
        raise CitasNotExistsError("No existe el tramite o servicio")
    if pag_tramite_servicio.estatus != "A":
        raise CitasIsDeletedError("No es activo el tramite o servicio, está eliminado")
    return pag_tramite_servicio
