"""
Cit Horas Bloqueadas V2, CRUD (create, read, update, and delete)
"""

from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from ...models.cit_horas_bloqueadas import CitHoraBloqueada
from .oficinas import get_oficina


def get_horas_bloquedas(db: Session, oficina_id: int, fecha: date) -> Any:
    """Consultar las horas bloqueadas de una oficina en una fecha dada"""
    consulta = db.query(CitHoraBloqueada)

    # Filtro por oficina
    oficina = get_oficina(db, oficina_id)
    consulta = consulta.filter(CitHoraBloqueada.oficina == oficina)

    # Filtro por fecha
    consulta = consulta.filter(CitHoraBloqueada.fecha == fecha)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitHoraBloqueada.id)
