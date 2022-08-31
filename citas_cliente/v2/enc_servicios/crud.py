"""
Encuestas Servicios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import EncServicio


def get_enc_servicios(db: Session) -> Any:
    """Consultar las encuestas de servicios activas"""
    consulta = db.query(EncServicio)
    return consulta.filter_by(estatus="A").order_by(EncServicio.id)


def get_enc_servicio(db: Session, enc_servicio_id: int) -> EncServicio:
    """Consultar una encuesta de servicio por su id"""
    enc_servicio = db.query(EncServicio).get(enc_servicio_id)
    if enc_servicio is None:
        raise IndexError("No existe ese encuesta de servicio")
    if enc_servicio.estatus != "A":
        raise IndexError("No es activo ese encuesta de servicio, está eliminado")
    return enc_servicio
