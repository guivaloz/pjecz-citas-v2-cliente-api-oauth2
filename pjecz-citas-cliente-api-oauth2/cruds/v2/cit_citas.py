"""
Cit Citas V2, CRUD (create, read, update, and delete)
"""

from datetime import date, datetime, time, timedelta
from typing import Any

from sqlalchemy.orm import Session

from ...dependencies.pwgen import generar_codigo_asistencia
from ...dependencies.redis import task_queue
from ...dependencies.safe_string import safe_string
from ...models.cit_citas import CitCita
from ...schemas.v2.cit_citas import CitCitaOut
from ...settings import LIMITE_CITAS_PENDIENTES
from .cit_citas_anonimas import get_cit_citas_anonimas
from .cit_clientes import get_cit_cliente
from .cit_dias_disponibles import get_cit_dias_disponibles
from .cit_dias_inhabiles import get_cit_dias_inhabiles
from .cit_horas_disponibles import get_cit_horas_disponibles
from .cit_oficinas_servicios import get_cit_oficinas_servicios
from .cit_servicios import get_cit_servicio
from .oficinas import get_oficina


def get_cit_citas(
    db: Session,
    cit_cliente_id: int,
) -> Any:
    """Consultar las citas del cliente, desde hoy y con estado PENDIENTE"""
    consulta = db.query(CitCita)

    # Consultar el cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)
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
    return consulta.filter_by(estatus="A").order_by(CitCita.inicio)


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


def get_cit_citas_disponibles_cantidad(
    db: Session,
    cit_cliente_id: int,
) -> int:
    """Consultar la cantidad de citas que puede agendar (que es su limite menos las pendientes)"""

    # Consultar el cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)

    # Definir la cantidad limite de citas del cliente
    limite = LIMITE_CITAS_PENDIENTES
    if cit_cliente.limite_citas_pendientes > limite:
        limite = cit_cliente.limite_citas_pendientes

    # Consultar las citas PENDIENTES
    citas_pendientes_cantidad = get_cit_citas(db=db, cit_cliente_id=cit_cliente_id).count()

    # Entregar la cantidad de citas disponibles que puede agendar
    if citas_pendientes_cantidad >= limite:
        return 0
    return limite - citas_pendientes_cantidad


def cancel_cit_cita(
    db: Session,
    cit_cliente_id: int,
    cit_cita_id: int,
) -> CitCitaOut:
    """Cancelar una cita"""

    # Consultar
    cit_cita = get_cit_cita(db, cit_cliente_id, cit_cita_id)

    # Validar que el estado sea PENDIENTE
    if cit_cita.estado != "PENDIENTE":
        raise ValueError("No se puede cancelar esta cita porque no esta pendiente")

    # Validar que se pueda cancelar
    if cit_cita.puede_cancelarse is False:
        raise ValueError("No se puede cancelar esta cita")

    # Actualizar registro
    cit_cita.estado = "CANCELO"
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # Agregar tarea en el fondo para que se envie un mensaje via correo electronico
    task_queue.enqueue(
        "citas_admin.blueprints.cit_citas.tasks.enviar_cancelado",
        cit_cita_id=cit_cita.id,
    )

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

    # Consultar y validar el cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)

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

    # Validar la hora_minuto, respecto a las horas disponibles
    if hora_minuto not in get_cit_horas_disponibles(db, oficina_id=oficina_id, cit_servicio_id=cit_servicio_id, fecha=fecha):
        raise ValueError("No es valida la hora-minuto porque no esta disponible")

    # Validar que las citas en ese tiempo para esa oficina NO hayan llegado al limite de personas
    cit_citas_anonimas = get_cit_citas_anonimas(db, oficina_id=oficina_id, fecha=fecha, hora_minuto=hora_minuto)
    if cit_citas_anonimas.count() >= oficina.limite_personas:
        raise ValueError("No se puede crear la cita porque ya se alcanzo el limite de personas en la oficina")

    # Validar que la cantidad de citas pendientes no haya llegado al limite de este cliente
    if get_cit_citas_disponibles_cantidad(db, cit_cliente_id=cit_cliente_id) <= 0:
        raise ValueError("No se puede crear la cita porque ya se alcanzo el limite de citas pendientes")

    # Definir los tiempos de la cita
    inicio_dt = datetime(year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute)
    termino_dt = datetime(
        year=fecha.year, month=fecha.month, day=fecha.day, hour=hora_minuto.hour, minute=hora_minuto.minute
    ) + timedelta(hours=cit_servicio.duracion.hour, minutes=cit_servicio.duracion.minute)

    # Validar que no tenga una cita pendiente en la misma fecha y hora
    for cit_cita in get_cit_citas(db, cit_cliente_id=cit_cliente_id).all():
        if cit_cita.inicio == inicio_dt:
            raise ValueError("No se puede crear la cita porque ya tiene una cita pendiente en esta fecha y hora")

    # Definir cancelar_antes con 24 horas antes de la cita
    cancelar_antes = inicio_dt - timedelta(hours=24)

    # Si cancelar_antes es un dia inhabil, domingo o sabado, se busca el dia habil anterior
    dias_inhabiles = get_cit_dias_inhabiles(db=db).all()
    while cancelar_antes.date() in dias_inhabiles or cancelar_antes.weekday() == 6 or cancelar_antes.weekday() == 5:
        if cancelar_antes.date() in dias_inhabiles:
            cancelar_antes = cancelar_antes - timedelta(days=1)
        if cancelar_antes.weekday() == 6:  # Si es domingo, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=2)
        if cancelar_antes.weekday() == 5:  # Si es sábado, se cambia a viernes
            cancelar_antes = cancelar_antes - timedelta(days=1)

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
        codigo_asistencia=generar_codigo_asistencia(),
        cancelar_antes=cancelar_antes,
    )
    db.add(cit_cita)
    db.commit()
    db.refresh(cit_cita)

    # Agregar tarea en el fondo para que se envie un mensaje via correo electronico
    task_queue.enqueue(
        "citas_admin.blueprints.cit_citas.tasks.enviar_pendiente",
        cit_cita_id=cit_cita.id,
    )

    # Entregar
    return cit_cita
