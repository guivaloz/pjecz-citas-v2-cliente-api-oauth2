"""
Tres de Tres - Partidos V3, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from ...dependencies.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from ...dependencies.hashids import descifrar_id
from ...dependencies.safe_string import safe_clave
from ...models.tdt_partidos import TdtPartido


def get_tdt_partidos(db: Session) -> Any:
    """Consultar los partidos activos"""
    return db.query(TdtPartido).filter_by(estatus="A").order_by(TdtPartido.siglas)


def get_tdt_partido(db: Session, tdt_partido_id: int) -> TdtPartido:
    """Consultar un partido por su id"""
    tdt_partido = db.query(TdtPartido).get(tdt_partido_id)
    if tdt_partido is None:
        raise CitasNotExistsError("No existe ese partido")
    if tdt_partido.estatus != "A":
        raise CitasIsDeletedError("No es activo ese partido, está eliminado")
    return tdt_partido


def get_tdt_partido_from_id_hasheado(db: Session, tdt_partido_id_hasheado: str) -> TdtPartido:
    """Consultar un partido por su id hasheado"""
    tdt_partido_id = descifrar_id(tdt_partido_id_hasheado)
    if tdt_partido_id is None:
        raise CitasNotValidParamError("El ID del partido no es válido")
    return get_tdt_partido(db, tdt_partido_id)


def get_tdt_partido_from_siglas(db: Session, siglas: str) -> TdtPartido:
    """Consultar un partido por sus siglas"""
    try:
        siglas = safe_clave(siglas)
    except ValueError as error:
        raise CitasNotValidParamError("Son incorrectas la siglas del partido") from error
    tdt_partido = db.query(TdtPartido).filter_by(siglas=siglas).first()
    if tdt_partido is None:
        raise CitasNotExistsError("No existe el partido")
    if tdt_partido.estatus != "A":
        raise CitasIsDeletedError("No es activo el partido, está eliminado")
    return tdt_partido
