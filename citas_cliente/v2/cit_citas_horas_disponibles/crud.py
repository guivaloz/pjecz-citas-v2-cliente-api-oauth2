"""
Cit Citas Horas Disponibles V2, CRUD (create, read, update, and delete)
"""
from datetime import date, timedelta, datetime, time
from typing import Any
from sqlalchemy.orm import Session


def get_cit_citas_horas_disponibles(
    db: Session,
    oficina_id: int = None,
    fecha: date = None,
) -> Any:
    """Consultar las horas disponibles, entrega un listado de horas"""
    horas_disponibles = []

    # Calcular horarios

    # Consultar las horas bloquedas

    # Revisar citas agendadas para la fecha

    # Quitar las horas bloqueadas

    # Quitar las horas ocupadas

    # Entregar
    return horas_disponibles
