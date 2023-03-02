"""
Distritos V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_clave, safe_string

from ...core.distritos.models import Distrito


def get_distritos(db: Session) -> Any:
    """Consultar los distritos activos"""
    return db.query(Distrito).filter_by(estatus="A").order_by(Distrito.nombre)


def get_distrito(db: Session, distrito_id: int) -> Distrito:
    """Consultar un distrito por su id"""
    distrito = db.query(Distrito).get(distrito_id)
    if distrito is None:
        raise CitasNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise CitasIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito


def get_distrito_from_id_hasheado(db: Session, distrito_id_hasheado: str) -> Distrito:
    """Consultar un distrito por su id hasheado"""
    distrito_id = descifrar_id(distrito_id_hasheado)
    if distrito_id is None:
        raise CitasNotValidParamError("El ID del distrito no es válido")
    return get_distrito(db, distrito_id)


def get_distrito_from_clave(db: Session, distrito_clave: str) -> Distrito:
    """Consultar un distrito por su clave"""
    try:
        clave = safe_clave(distrito_clave)
    except ValueError as error:
        raise CitasNotValidParamError("No es válida la clave del distrito") from error
    if clave == "":
        raise CitasNotValidParamError("No es válida la clave del distrito")
    distrito = db.query(Distrito).filter_by(clave=clave).first()
    if distrito is None:
        raise CitasNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise CitasIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito


def get_distrito_from_nombre(db: Session, distrito_nombre: str) -> Distrito:
    """Consultar un distrito por su nombre"""
    nombre = safe_string(distrito_nombre, save_enie=True, to_uppercase=True)
    if nombre == "":
        raise CitasNotValidParamError("No es válido el nombre del distrito")
    distrito = db.query(Distrito).filter_by(nombre=nombre).first()
    if distrito is None:
        raise CitasNotExistsError("No existe ese distrito")
    if distrito.estatus != "A":
        raise CitasIsDeletedError("No es activo ese distrito, está eliminado")
    return distrito
