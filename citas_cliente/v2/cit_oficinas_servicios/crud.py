"""
Cit Oficinas Servicios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from ...core.cit_oficinas_servicios.models import CitOficinaServicio
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_oficinas_servicios(
    db: Session,
    cit_servicio_id: int = None,
    oficina_id: int = None,
) -> Any:
    """Consultar los oficinas-servicios activos"""
    consulta = db.query(CitOficinaServicio)
    if cit_servicio_id:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
        consulta = consulta.filter(CitOficinaServicio.cit_servicio == cit_servicio)
    if oficina_id:
        oficina = get_oficina(db, oficina_id)
        consulta = consulta.filter(CitOficinaServicio.oficina == oficina)
    return consulta.filter_by(estatus="A").order_by(CitOficinaServicio.id)


def get_cit_oficina_servicio(db: Session, cit_oficina_servicio_id: int) -> CitOficinaServicio:
    """Consultar un oficina-servicio por su id"""
    cit_oficina_servicio = db.query(CitOficinaServicio).get(cit_oficina_servicio_id)
    if cit_oficina_servicio is None:
        raise IndexError("No existe ese oficina-servicio")
    if cit_oficina_servicio.estatus != "A":
        raise IndexError("No es activo ese oficina-servicio, está eliminado")
    return cit_oficina_servicio
