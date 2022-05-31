"""
Cit Dias Disponibles V2, CRUD (create, read, update, and delete)
"""
from datetime import date, timedelta
from typing import Any
from sqlalchemy.orm import Session

from ..cit_dias_inhabiles.crud import get_cit_dias_inhabiles

LIMITE_DIAS = 90


def get_cit_dias_disponibles(
    db: Session,
    oficina_id: int,
) -> Any:
    """Consultar los dias disponibles, entrega un listado de fechas"""
    dias_disponibles = []

    # Consultar dias inhabiles
    cit_dias_inhabiles = get_cit_dias_inhabiles(db).all()
    dias_inhabiles = []
    if len(cit_dias_inhabiles) > 0:
        dias_inhabiles = [item.fecha for item in cit_dias_inhabiles]

    # Agregar cada dia hasta el limite a partir de manana
    for fecha in (date.today() + timedelta(n) for n in range(1, LIMITE_DIAS)):

        # Quitar los sabados y domingos
        if fecha.weekday() in (5, 6):
            continue

        # Quitar los dias inhabiles
        if fecha in dias_inhabiles:
            continue

        # Acumular
        dias_disponibles.append(fecha)

    # Entregar
    return dias_disponibles
