"""
Cit Clientes V2, CRUD (create, read, update, and delete)
"""
import hashlib
import re
from typing import Any
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from lib.safe_string import CURP_REGEXP, EMAIL_REGEXP, PASSWORD_REGEXP, PASSWORD_REGEXP_MESSAGE

from .models import CitCliente
from .schemas import CitClienteActualizarContrasenaIn


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


def get_cit_cliente_from_curp(db: Session, cliente_curp: str) -> CitCliente:
    """Consultar un cliente por su curp"""
    if re.match(CURP_REGEXP, cliente_curp) is None:
        raise ValueError("El CURP no es valido")
    cit_cliente = db.query(CitCliente).filter_by(curp=cliente_curp).first()
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise IndexError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_email(db: Session, cliente_email: str) -> CitCliente:
    """Consultar un cliente por su id"""
    if re.match(EMAIL_REGEXP, cliente_email) is None:
        raise ValueError("El correo electronico no es valido")
    cit_cliente = db.query(CitCliente).filter_by(email=cliente_email).first()
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise IndexError("No es activo ese cliente, está eliminado")
    return cit_cliente


def update_cit_cliente_password(db: Session, actualizacion: CitClienteActualizarContrasenaIn) -> CitCliente:
    """Actualizar la contrasena de la version 1 a la version 2"""
    # Validar el correo electronico
    if re.match(EMAIL_REGEXP, actualizacion.email) is None:
        raise ValueError("El correo electronico no es valido")
    # Validar la contrasena nueva
    if re.match(PASSWORD_REGEXP, actualizacion.contrasena_nueva) is None:
        raise ValueError(PASSWORD_REGEXP_MESSAGE)
    # Validar que exista el cliente
    cit_cliente = db.query(CitCliente).filter_by(email=actualizacion.email).filter_by(estatus="A").first()
    if cit_cliente is None:
        raise IndexError("No existe ese cliente")
    # Validar la contrasena anterior
    contrasena_anterior_md5 = hashlib.md5(actualizacion.contrasena_anterior.encode("utf-8")).hexdigest()
    if contrasena_anterior_md5 != cit_cliente.contrasena_md5:
        raise ValueError("La contrasena anterior no es correcta")
    # Poner en blanco la contrasena anterior
    cit_cliente.contrasena_md5 = ""
    # Cifrar la contrasena nueva
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")
    cit_cliente.contrasena_sha256 = pwd_context.hash(actualizacion.contrasena_nueva)
    # Actualizar el cliente
    db.add(cit_cliente)
    db.commit()
    # Entregar el cliente y el mensaje de exito
    cit_cliente.mensaje = "Contraseña actualizada"
    return cit_cliente
