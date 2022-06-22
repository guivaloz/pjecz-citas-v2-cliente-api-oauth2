"""
Cit Tramites Servicios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import CitTramiteServicio


def get_cit_tramites_servicios(db: Session) -> Any:
    """Consultar los tramites y servicios activos"""
    return db.query(CitTramiteServicio).filter_by(estatus="A").order_by(CitTramiteServicio.nombre)


def get_cit_tramite_servicio(db: Session, cit_tramite_servicio_id: int) -> CitTramiteServicio:
    """Consultar un tramite y servicio por su id"""
    cit_tramite_servicio = db.query(CitTramiteServicio).get(cit_tramite_servicio_id)
    if cit_tramite_servicio is None:
        raise IndexError("No existe ese tramite y servicio")
    if cit_tramite_servicio.estatus != "A":
        raise IndexError("No es activo ese tramite y servicio, está eliminado")
    return cit_tramite_servicio
