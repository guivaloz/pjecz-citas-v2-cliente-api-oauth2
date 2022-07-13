"""
Cit Horas Bloqueadas V2, CRUD (create, read, update, and delete)
"""
from datetime import date
from typing import Any
from sqlalchemy.orm import Session

from ..oficinas.crud import get_oficina
from .models import CitHoraBloqueada


def get_horas_bloquedas(db: Session, oficina_id: int, fecha: date) -> Any:
    """Consultar las horas bloqueadas de una oficina en una fecha dada"""
    consulta = db.query(CitHoraBloqueada)

    # Filtro por oficina
    oficina = get_oficina(db, oficina_id)  # Causara index error si no existe, esta eliminada o no puede agendar citas
    consulta = consulta.filter(CitHoraBloqueada.oficina == oficina)

    # Filtro por fecha
    consulta = consulta.filter(CitHoraBloqueada.fecha == fecha)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitHoraBloqueada.id)
