"""
Municipios V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.hashids import descifrar_id

from ...core.municipios.models import Municipio


def get_municipios(db: Session) -> Any:
    """Consultar los municipios activos"""
    return db.query(Municipio).filter_by(estatus="A").order_by(Municipio.nombre)


def get_municipio(db: Session, municipio_id: int) -> Municipio:
    """Consultar un municipio por su id"""
    municipio = db.query(Municipio).get(municipio_id)
    if municipio is None:
        raise CitasNotExistsError("No existe ese municipio")
    if municipio.estatus != "A":
        raise CitasIsDeletedError("No es activo ese municipio, está eliminado")
    return municipio


def get_municipio_from_id_hasheado(db: Session, municipio_id_hasheado: str) -> Municipio:
    """Consultar un municipio por su id_hasheado"""
    municipio_id = descifrar_id(municipio_id_hasheado)
    if municipio_id is None:
        raise CitasNotExistsError("El ID del pago no es válido")
    return get_municipio(db, municipio_id)
