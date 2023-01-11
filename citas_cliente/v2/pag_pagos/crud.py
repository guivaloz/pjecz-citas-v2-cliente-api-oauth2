"""
Pag Pagos V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string

from .models import PagPago
from ..cit_clientes.crud import get_cit_cliente


def get_pag_pagos(
    db: Session,
    cit_cliente_id: int,
    estado: str = None,
) -> Any:
    """Consultar los pagos activos"""

    # Consulta
    consulta = db.query(PagPago)

    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(PagPago.cit_cliente == cit_cliente)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado in PagPago.ESTADOS:
            consulta = consulta.filter_by(estado=estado)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(PagPago.id)


def get_pag_pago(
    db: Session,
    cit_cliente_id: int,
    pag_pago_id: int,
) -> PagPago:
    """Consultar un pago por su id"""

    # Consultar
    pag_pago = db.query(PagPago).get(pag_pago_id)

    # Validar
    if pag_pago is None:
        raise IndexError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")
    if pag_pago.cit_cliente_id != cit_cliente_id:
        raise ValueError("No le pertenece esta cita")

    # Entregar
    return pag_pago
