"""
Cit Dias Inhabiles V2, CRUD (create, read, update, and delete)
"""

from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from ...models.cit_dias_inhabiles import CitDiaInhabil


def get_cit_dias_inhabiles(db: Session) -> Any:
    """Consultar los dias inhabiles activos"""
    consulta = db.query(CitDiaInhabil)

    # Filtrar por fechas en el futuro
    consulta = consulta.filter(CitDiaInhabil.fecha >= date.today())

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitDiaInhabil.id)
