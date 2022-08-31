"""
Encuestas Sistemas V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import EncSistema


def get_enc_sistemas(db: Session) -> Any:
    """Consultar las encuestas de sistemas activas"""
    consulta = db.query(EncSistema)
    return consulta.filter_by(estatus="A").order_by(EncSistema.id)


def get_enc_sistema(db: Session, enc_sistema_id: int) -> EncSistema:
    """Consultar una encuesta de sistemas por su id"""
    enc_sistema = db.query(EncSistema).get(enc_sistema_id)
    if enc_sistema is None:
        raise IndexError("No existe ese encuesta de sistemas")
    if enc_sistema.estatus != "A":
        raise IndexError("No es activo ese encuesta de sistemas, está eliminado")
    return enc_sistema
