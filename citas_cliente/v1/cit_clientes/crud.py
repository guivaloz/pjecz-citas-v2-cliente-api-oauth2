"""
Cit Clientes v1, CRUD (create, read, update, and delete)
"""
import re
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import CURP_REGEXP, EMAIL_REGEXP

from .models import CitCliente


def get_cit_clientes(db: Session) -> Any:
    """Consultar los clientes activos"""
    consulta = db.query(CitCliente)
    return consulta.filter_by(estatus="A").order_by(CitCliente.id)


def get_cit_cliente(db: Session, cit_cliente_id: int) -> CitCliente:
    """Consultar un cliente por su id"""
    cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise ValueError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_curp(db: Session, curp: str) -> CitCliente:
    """Consultar un cliente por su curp"""
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP no es valido")
    cit_cliente = db.query(CitCliente).filter_by(curp=curp).first()
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise ValueError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_email(db: Session, email: str) -> CitCliente:
    """Consultar un cliente por su id"""
    if re.match(EMAIL_REGEXP, email) is None:
        raise ValueError("El correo electronico no es valido")
    cit_cliente = db.query(CitCliente).filter_by(email=email).first()
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise ValueError("No es activo ese cliente, está eliminado")
    return cit_cliente
