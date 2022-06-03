"""
Cit Citas V2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime
from typing import Any
from sqlalchemy.orm import Session

from ..cit_clientes.crud import get_cit_cliente
from ..oficinas.crud import get_oficina
from .models import CitCita


def get_cit_citas(
    db: Session,
    cit_cliente_id: int,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)

    # Consultar el cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)  # Causara index error si no existe o esta eliminada
    consulta = consulta.filter(CitCita.cit_cliente == cit_cliente)

    # Se consultan todas los citas desde hoy
    fecha = date.today()

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

    # Entregar
    return consulta.filter_by(estatus="A").order_by(CitCita.id)


def get_cit_citas_anonimas(
    db: Session,
    oficina_id: int,
    fecha: date,
) -> Any:
    """Consultar los citas activos"""
    consulta = db.query(CitCita)

    # Filtrar por la oficina
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
