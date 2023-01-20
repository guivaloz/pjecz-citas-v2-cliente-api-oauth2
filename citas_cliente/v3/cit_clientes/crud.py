"""
Cit Clientes V3, CRUD (create, read, update, and delete)
"""
from typing import Any

from sqlalchemy.orm import Session

from lib.exceptions import CitasIsDeletedError, CitasNotExistsError
from lib.safe_string import safe_curp, safe_email

from ...core.cit_clientes.models import CitCliente


def get_cit_clientes(db: Session) -> Any:
    """Consultar los clientes activos"""
    consulta = db.query(CitCliente)
    return consulta.filter_by(estatus="A").order_by(CitCliente.id)


def get_cit_cliente(db: Session, cit_cliente_id: int) -> CitCliente:
    """Consultar un cliente por su id"""
    cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_curp(db: Session, cliente_curp: str) -> CitCliente:
    """Consultar un cliente por su curp"""
    cliente_curp = safe_curp(cliente_curp)
    cit_cliente = db.query(CitCliente).filter_by(curp=cliente_curp).first()
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_email(db: Session, cliente_email: str) -> CitCliente:
    """Consultar un cliente por su email"""
    cliente_email = safe_email(cliente_email)
    cit_cliente = db.query(CitCliente).filter_by(email=cliente_email).first()
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente
