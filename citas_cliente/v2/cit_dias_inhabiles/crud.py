"""
Cit Dias Inhabiles V2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from .models import CitDiaInhabil


def get_cit_dias_inhabiles(db: Session) -> Any:
    """Consultar los dias inhabiles activos"""
    consulta = db.query(CitDiaInhabil)
    consulta.filter(CitDiaInhabil.fecha >= date.today())
    return consulta.filter_by(estatus="A").order_by(CitDiaInhabil.id)
