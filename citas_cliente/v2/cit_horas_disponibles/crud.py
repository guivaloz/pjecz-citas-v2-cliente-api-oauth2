"""
Cit Horas Disponibles V2, CRUD (create, read, update, and delete)
"""
from datetime import date, timedelta, datetime, time
from typing import Any
from sqlalchemy.orm import Session

from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina


def get_cit_horas_disponibles(
    db: Session,
    oficina_id: int,
    cit_servicio_id: int,
    fecha: date,
) -> Any:
    """Consultar las horas disponibles, entrega un listado de horas"""
    horas_disponibles = []

    # Consultar oficina
    oficina = get_oficina(db, oficina_id)  # Causara index error si no existe, esta eliminada o no puede agendar citas

    # Consultar el servicio
    cit_servicio = get_cit_servicio(db, cit_servicio_id)

    # Validar fecha

    # Definir los tiempos de inicio, de termino y el timedelta de la duracion
    tiempo_inicial = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=oficina.apertura.hour,
        minute=oficina.apertura.minute,
        second=0,
    )
    tiempo_final = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=oficina.cierre.hour,
        minute=oficina.cierre.minute,
        second=0,
    )
    duracion = timedelta(
        hours=cit_servicio.duracion.hour,
        minutes=cit_servicio.duracion.minute,
    )

    # Consultar las horas bloquedas

    # Revisar citas agendadas para la fecha

    # Bucle por los intervalos
    tiempo = tiempo_inicial
    while tiempo <= tiempo_final:
        # Quitar las horas bloqueadas
        # Quitar las horas ocupadas
        # Acumular
        horas_disponibles.append(tiempo.time())
        # Siguiente intervalo
        tiempo = tiempo + duracion

    # Quitar la ultima hora disponible
    horas_disponibles.pop()

    # Entregar
    return horas_disponibles
