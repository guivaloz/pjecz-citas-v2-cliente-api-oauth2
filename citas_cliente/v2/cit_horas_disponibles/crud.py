"""
Cit Horas Disponibles V2, CRUD (create, read, update, and delete)
"""
from datetime import date, timedelta, datetime
from typing import Any
from sqlalchemy.orm import Session

from ..cit_citas.crud import get_cit_citas_anonimas
from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles
from ..cit_horas_bloqueadas.crud import get_horas_bloquedas
from ..cit_servicios.crud import get_cit_servicio
from ..oficinas.crud import get_oficina

LIMITE_DIAS = 90


def get_cit_horas_disponibles(
    db: Session,
    oficina_id: int,
    cit_servicio_id: int,
    fecha: date,
) -> Any:
    """Consultar las horas disponibles, entrega un listado de horas"""

    # Consultar oficina
    oficina = get_oficina(db, oficina_id)  # Causara index error si no existe, esta eliminada o no puede agendar citas

    # Consultar el servicio
    cit_servicio = get_cit_servicio(db, cit_servicio_id)

    # Validar que la fecha no sea del pasado
    if fecha <= date.today():
        raise ValueError("No puede agendar citas para hoy o en el pasado")

    # Validar que la fecha no sea posterior al LIMITE_DIAS
    if fecha > date.today() + timedelta(LIMITE_DIAS):
        raise ValueError(f"No puede agendar citas en mas de {LIMITE_DIAS} dias")

    # Validar que la fecha no sea sabado o domingo
    if fecha.weekday() in (5, 6):
        raise ValueError("No puede agendar citas en fines de semana")

    # Validar que la fecha no sea un dia inhabil
    cit_dias_inhabiles = get_cit_dias_inhabiles(db).all()
    dias_inhabiles = [item.fecha for item in cit_dias_inhabiles]
    if fecha in dias_inhabiles:
        raise ValueError("No puede agendar citas en dias inhabiles")

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

    # Consultar las horas bloquedas y convertirlas a datetime para compararlas
    tiempos_bloqueados = []
    cit_horas_bloqueadas = get_horas_bloquedas(db, oficina_id=oficina_id, fecha=fecha).all()
    for cit_hora_bloqueada in cit_horas_bloqueadas:
        tiempos_bloqueados.append(
            datetime(
                year=fecha.year,
                month=fecha.month,
                day=fecha.day,
                hour=cit_hora_bloqueada.inicio.hour,
                minute=cit_hora_bloqueada.inicio.minute,
                second=0,
            )
        )

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
        if tiempo in tiempos_bloqueados:
            es_hora_disponible = False
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
