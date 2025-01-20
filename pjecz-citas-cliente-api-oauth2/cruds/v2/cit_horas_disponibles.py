"""
Cit Horas Disponibles V2, CRUD (create, read, update, and delete)
"""

from datetime import date, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from .cit_citas_anonimas import get_cit_citas_anonimas
from .cit_dias_disponibles import get_cit_dias_disponibles
from .cit_horas_bloqueadas import get_horas_bloquedas
from .cit_servicios import get_cit_servicio
from .oficinas import get_oficina

LIMITE_DIAS = 90


def get_cit_horas_disponibles(
    db: Session,
    oficina_id: int,
    cit_servicio_id: int,
    fecha: date,
) -> Any:
    """Consultar las horas disponibles, entrega un listado de horas"""

    # Consultar oficina
    oficina = get_oficina(db, oficina_id)

    # Consultar el servicio
    cit_servicio = get_cit_servicio(db, cit_servicio_id)

    # Validar la fecha, debe ser un dia disponible
    if fecha not in get_cit_dias_disponibles(db, oficina_id=oficina_id):
        raise ValueError("No es valida la fecha")

    # Tomar los tiempos de inicio y termino de la oficina
    apertura = oficina.apertura
    cierre = oficina.cierre

    # Si el servicio tiene un tiempo desde
    if cit_servicio.desde and apertura < cit_servicio.desde:
        apertura = cit_servicio.desde

    # Si el servicio tiene un tiempo hasta
    if cit_servicio.hasta and cierre > cit_servicio.hasta:
        cierre = cit_servicio.hasta

    # Definir los tiempos de inicio, de final y el timedelta de la duracion
    tiempo_inicial = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=apertura.hour,
        minute=apertura.minute,
        second=0,
    )
    tiempo_final = datetime(
        year=fecha.year,
        month=fecha.month,
        day=fecha.day,
        hour=cierre.hour,
        minute=cierre.minute,
        second=0,
    )
    duracion = timedelta(
        hours=cit_servicio.duracion.hour,
        minutes=cit_servicio.duracion.minute,
    )

    # Consultar las horas bloquedas y convertirlas a datetime para compararlas
    tiempos_bloqueados = []
    cit_horas_bloqueadas = get_horas_bloquedas(db, oficina_id=oficina_id, fecha=fecha).all()
    for cit_hora_bloqueada in cit_horas_bloqueadas:
        tiempo_bloquedo_inicia = datetime(
            year=fecha.year,
            month=fecha.month,
            day=fecha.day,
            hour=cit_hora_bloqueada.inicio.hour,
            minute=cit_hora_bloqueada.inicio.minute,
            second=0,
        )
        tiempo_bloquedo_termina = datetime(
            year=fecha.year,
            month=fecha.month,
            day=fecha.day,
            hour=cit_hora_bloqueada.termino.hour,
            minute=cit_hora_bloqueada.termino.minute,
            second=0,
        ) - timedelta(minutes=1)
        tiempos_bloqueados.append((tiempo_bloquedo_inicia, tiempo_bloquedo_termina))

    # Acumular las citas agendadas en un diccionario de tiempos y cantidad de citas, para la oficina en la fecha
    # { 08:30: 2, 08:45: 1, 10:00: 2,... }
    citas_ya_agendadas = {}
    for cit_cita in get_cit_citas_anonimas(db, oficina_id=oficina_id, fecha=fecha).all():
        if cit_cita.inicio not in citas_ya_agendadas:
            citas_ya_agendadas[cit_cita.inicio] = 1
        else:
            citas_ya_agendadas[cit_cita.inicio] += 1

    # Bucle por los intervalos
    horas_minutos_segundos_disponibles = []
    tiempo = tiempo_inicial
    while tiempo < tiempo_final:
        # Bandera
        es_hora_disponible = True
        # Quitar las horas bloqueadas
        for tiempo_bloqueado in tiempos_bloqueados:
            if tiempo_bloqueado[0] <= tiempo <= tiempo_bloqueado[1]:
                es_hora_disponible = False
                break
        # Quitar las horas ocupadas
        if tiempo in citas_ya_agendadas:
            if citas_ya_agendadas[tiempo] >= oficina.limite_personas:
                es_hora_disponible = False
        # Acumular si es hora disponible
        if es_hora_disponible:
            horas_minutos_segundos_disponibles.append(tiempo.time())
        # Siguiente intervalo
        tiempo = tiempo + duracion

    # Que hacer cuando no haya horas_minutos_segundos_disponibles
    if len(horas_minutos_segundos_disponibles) == 0:
        raise ValueError("No hay horas disponibles")

    # Entregar
    return horas_minutos_segundos_disponibles
