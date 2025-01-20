"""
Oficinas V2, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from ...models.oficinas import Oficina
from .distritos import get_distrito


def get_oficinas(db: Session, distrito_id: int = None) -> Any:
    """Consultar las oficinas activas"""
    consulta = db.query(Oficina)
    if distrito_id:
        distrito = get_distrito(db, distrito_id)  # Validar que exista el distrito
        consulta = consulta.filter(Oficina.distrito == distrito)
    return consulta.filter_by(estatus="A").filter_by(puede_agendar_citas=True).order_by(Oficina.clave)


def get_oficina(db: Session, oficina_id: int) -> Oficina:
    """Consultar una oficina por su id"""
    oficina = db.query(Oficina).get(oficina_id)
    if oficina is None:
        raise IndexError("No existe ese oficina")
    if oficina.estatus != "A":
        raise IndexError("No es activo ese oficina, está eliminado")
    if oficina.puede_agendar_citas is False:
        raise IndexError("No puede agendar citas en esta oficina")
    return oficina
