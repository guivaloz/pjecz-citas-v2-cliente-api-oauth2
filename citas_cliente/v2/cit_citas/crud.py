"""
Cit Citas V2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string

from ..cit_clientes.crud import get_cit_cliente
from ..oficinas.crud import get_oficina
from .models import CitCita
from .schemas import CitCitaOut

from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina

LIMITE_DIAS = 90


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


def get_cit_cita(db: Session, cit_cliente_id: int, cit_cita_id: int) -> CitCitaOut:
    """Consultar una cita"""

    # Consultar
    cit_cita = db.query(CitCita).get(cit_cita_id)

    # Validar
    if cit_cita is None:
        raise IndexError("No existe esa cita")
    if cit_cita.estatus != "A":
        raise ValueError("No es activa esa cita, está eliminado")
    if cit_cita.cit_cliente_id != cit_cliente_id:
        raise ValueError("No le pertenece esta cita")

    # Entregar
    return cit_cita


def cancel_cit_cita(db: Session, cit_cliente_id: int, cit_cita_id: int) -> CitCitaOut:
    """Cancelar una cita"""

    # Consultar
    cit_cita = get_cit_cita(db, cit_cliente_id, cit_cita_id)

    # Actualizar registro
    cit_cita.estado = "CANCELO"
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # Entregar
    return cit_cita


def create_cit_cita(
    db: Session,
    cit_cliente_id: int,
    oficina_id: int,
    cit_servicio_id: int,
    fecha: date,
    hora_minuto: time,
    nota: str,
) -> CitCitaOut:
    """Crear una cita"""

    # Consultar y validar la oficina
    oficina = get_oficina(db, oficina_id=oficina_id)

    # Consultar y validar el servicio
    cit_servicio = get_cit_servicio(db, cit_servicio_id=cit_servicio_id)

    # Validar que ese servicio lo ofrezca esta oficina

    # Validar la fecha, debe desde manana

    # Validar la fecha, no debe de pasar de LIMITE_DIAS

    # Validar la hora_minuto, debe de estar dentro del horario de la oficina

    # Definir el inicio
    inicio_dt = None

    # Definir el termino
    termino_dt = None

    # Insertar registro
    cit_cita = CitCita(
        cit_servicio_id=cit_servicio.id,
        cit_cliente_id=cit_cliente_id,
        oficina_id=oficina.id,
        inicio=inicio_dt,
        termino=termino_dt,
        notas=safe_string(input_str=nota, max_len=512),
        estado="PENDIENTE",
        asistencia=False,
    )
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # Entregar
    return cit_cita
