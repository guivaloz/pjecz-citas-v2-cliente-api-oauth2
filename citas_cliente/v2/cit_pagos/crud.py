"""
Cit Pagos V2, CRUD (create, read, update, and delete)
"""
from typing import Any
from sqlalchemy.orm import Session

from .models import CitPago
from ..cit_clientes.crud import get_cit_cliente


def get_cit_pagos(db: Session, cit_cliente_id: int) -> Any:
    """Consultar los pagos activos"""
    consulta = db.query(CitPago)
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)
    consulta = consulta.filter(CitPago.cit_cliente == cit_cliente)
    return consulta.filter_by(estatus="A").order_by(CitPago.id)


def get_cit_pago(db: Session, cit_pago_id: int) -> CitPago:
    """Consultar un pago por su id"""
    cit_pago = db.query(CitPago).get(cit_pago_id)
    if cit_pago is None:
        raise IndexError("No existe ese pago")
    if cit_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")
    return cit_pago
