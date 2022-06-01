"""
Cit Citas V2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any
from sqlalchemy.orm import Session

from ..oficinas.crud import get_oficina
from .models import CitCita


def get_cit_citas(
    db: Session,
    oficina_id: int,
    fecha: date,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)

    # Filtro por oficina
    oficina = get_oficina(db, oficina_id)  # Causara index error si no existe, esta eliminada o no puede agendar citas
    consulta = consulta.filter(CitCita.oficina == oficina)

    # Filtro por tiempo de inicio
    desde_tiempo = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=0,
        minute=0,
        second=0,
    )
    consulta = consulta.filter(CitCita.inicio >= desde_tiempo)

    # Filtro por tiempo de termino
    hasta_tiempo = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=23,
        minute=59,
        second=59,
    )
    consulta = consulta.filter(CitCita.termino <= hasta_tiempo)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCita.id)
