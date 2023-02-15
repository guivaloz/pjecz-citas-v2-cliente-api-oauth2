"""
Autoridades V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.safe_string import safe_clave

from ...core.autoridades.models import Autoridad


def get_autoridades(db: Session) -> Any:
    """Consultar los autoridades activos"""
    return db.query(Autoridad).filter_by(estatus="A").order_by(Autoridad.id)


def get_autoridad(db: Session, autoridad_id: int) -> Autoridad:
    """Consultar un autoridad por su id"""
    autoridad = db.query(Autoridad).get(autoridad_id)
    if autoridad is None:
        raise CitasNotExistsError("No existe ese autoridad")
    if autoridad.estatus != "A":
        raise CitasIsDeletedError("No es activo ese autoridad, está eliminado")
    return autoridad


def get_autoridad_from_clave(db: Session, clave: str) -> Autoridad:
    """Consultar un autoridad por su clave"""
    try:
        clave = safe_clave(clave)
    except ValueError as error:
        raise ValueError("Es incorrecta la clave del autoridad") from error
    autoridad = db.query(Autoridad).filter_by(clave=clave).first()
    if autoridad is None:
        raise CitasNotExistsError("No existe el autoridad")
    if autoridad.estatus != "A":
        raise CitasIsDeletedError("No es activo el autoridad, está eliminado")
    return autoridad
