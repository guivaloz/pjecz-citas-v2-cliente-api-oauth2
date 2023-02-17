"""
Tres de Tres - Partidos V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.safe_string import safe_clave

from ...core.tdt_partidos.models import TdtPartido


def get_tdt_partidos(db: Session) -> Any:
    """Consultar los partidos activos"""
    return db.query(TdtPartido).filter_by(estatus="A").order_by(TdtPartido.id)


def get_tdt_partido(db: Session, tdt_partido_id: int) -> TdtPartido:
    """Consultar un partido por su id"""
    tdt_partido = db.query(TdtPartido).get(tdt_partido_id)
    if tdt_partido is None:
        raise CitasNotExistsError("No existe ese partido")
    if tdt_partido.estatus != "A":
        raise CitasIsDeletedError("No es activo ese partido, está eliminado")
    return tdt_partido


def get_tdt_partido_from_siglas(db: Session, siglas: str) -> TdtPartido:
    """Consultar un partido por sus siglas"""
    try:
        siglas = safe_clave(siglas)
    except ValueError as error:
        raise ValueError("Son incorrectas la siglas del partido") from error
    tdt_partido = db.query(TdtPartido).filter_by(siglas=siglas).first()
    if tdt_partido is None:
        raise CitasNotExistsError("No existe el partido")
    if tdt_partido.estatus != "A":
        raise CitasIsDeletedError("No es activo el partido, está eliminado")
    return tdt_partido
