"""
Domicilios V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from ...core.domicilios.models import Domicilio


def get_domicilios(db: Session) -> Any:
    """Consultar los domicilios activos"""
    return db.query(Domicilio).filter_by(estatus="A").order_by(Domicilio.id)


def get_domicilio(db: Session, domicilio_id: int) -> Domicilio:
    """Consultar un domicilio por su id"""
    domicilio = db.query(Domicilio).get(domicilio_id)
    if domicilio is None:
        raise IndexError("No existe ese domicilio")
    if domicilio.estatus != "A":
        raise IndexError("No es activo ese domicilio, está eliminado")
    return domicilio
