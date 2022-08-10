"""
Cit Citas V2, CRUD (create, read, update, and delete)
"""
from datetime import date, datetime, time, timedelta
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string
from lib.redis import task_queue

from ..cit_citas_anonimas.crud import get_cit_citas_anonimas
from ..cit_clientes.crud import get_cit_cliente
from ..cit_dias_disponibles.crud import get_cit_dias_disponibles
from ..cit_horas_disponibles.crud import get_cit_horas_disponibles
from ..cit_oficinas_servicios.crud import get_cit_oficinas_servicios
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina
from .models import CitCita
from .schemas import CitCitaOut

LIMITE_CITAS_PENDIENTES = 30


def get_cit_citas(
    db: Session,
    cit_cliente_id: int,
) -> Any:
    """Consultar las citas del cliente, desde hoy y con estado PENDIENTE"""
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

    # Filtro por estado, solo PENDIENTE
    consulta = consulta.filter_by(estado="PENDIENTE")

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

    # Validar que el estado sea PENDIENTE
    if cit_cita.estado != "PENDIENTE":
        raise ValueError("No se puede cancelar esta cita porque no esta pendiente")

    # Validar la fecha, no debe ser de hoy o del pasado
    manana = date.today() + timedelta(days=1)
    if cit_cita.inicio < datetime(year=manana.year, month=manana.month, day=manana.day):
        raise ValueError("No se puede cancelar esta cita porque es de hoy o del pasado")

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
    cit_oficinas_servicios = get_cit_oficinas_servicios(db, oficina_id=oficina_id).all()
    if cit_servicio_id not in [cit_oficina_servicio.cit_servicio_id for cit_oficina_servicio in cit_oficinas_servicios]:
        raise ValueError("No es posible agendar este servicio en esta oficina")

    # Validar la fecha, debe ser un dia disponible
    if fecha not in get_cit_dias_disponibles(db, oficina_id=oficina_id):
        raise ValueError("No es valida la fecha")

    # Definir los tiempos de la oficina
    # oficina_apertura_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=oficina.apertura.hour, minute=oficina.apertura.minute)
    # oficina_cierre_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=oficina.cierre.hour, minute=oficina.cierre.minute)

    # Validar la hora_minuto, respecto a la apertura de la oficina
    # if inicio_dt < oficina_apertura_dt:
    #    raise ValueError("No es valida la hora-minuto porque es anterior a la apertura")
    # if termino_dt > oficina_cierre_dt:
    #    raise ValueError("No es valida la hora-minuto porque el termino es posterior al cierre")

    # Validar la hora_minuto, respecto a las horas disponibles
    if hora_minuto not in get_cit_horas_disponibles(db, oficina_id=oficina_id, cit_servicio_id=cit_servicio_id, fecha=fecha):
        raise ValueError("No es valida la hora-minuto porque no esta disponible")

    # Validar que las citas en ese tiempo para esa oficina NO hayan llegado al limite de personas
    cit_citas = get_cit_citas_anonimas(db, oficina_id=oficina_id, fecha=fecha, hora_minuto=hora_minuto)
    if cit_citas.count() >= oficina.limite_personas:
        raise ValueError("No se puede crear la cita porque ya se alcanzo el limite de personas")

    # Validar que la cantidad de citas pendientes no haya llegado al limite de este cliente
    cit_citas = get_cit_citas(db, cit_cliente_id=cit_cliente_id)
    if cit_citas.count() >= LIMITE_CITAS_PENDIENTES:
        raise ValueError("No se puede crear la cita porque ya se alcanzo su limite de citas pendientes")

    # Definir los tiempos de la cita
    inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute)
    termino_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute) + timedelta(hours=cit_servicio.duracion.hour, minutes=cit_servicio.duracion.minute)

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

    # Agregar tarea en el fondo para que se envie un mensaje via correo electronico
    task_queue.enqueue(
        "citas_admin.blueprints.cit_citas.tasks.enviar",
        cit_cita_id=cit_cita.id,
    )

    # Entregar
    return cit_cita
