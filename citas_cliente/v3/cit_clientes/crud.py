"""
Cit Clientes V3, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from config.settings import LIMITE_CITAS_PENDIENTES
from lib.exceptions import CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from lib.hashids import descifrar_id
from lib.safe_string import safe_curp, safe_email, safe_string, safe_telefono

from ...core.cit_clientes.models import CitCliente


def get_cit_clientes(db: Session) -> Any:
    """Consultar los clientes activos"""
    consulta = db.query(CitCliente)
    return consulta.filter_by(estatus="A").order_by(CitCliente.id)


def get_cit_cliente(db: Session, cit_cliente_id: int) -> Any:
    """Consultar un cliente por su id"""
    cit_cliente = db.query(CitCliente).get(cit_cliente_id)
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_id_hasheado(db: Session, cit_cliente_id_hasheado: str) -> CitCliente:
    """Consultar un cliente por su id hasheado"""
    cit_cliente_id = descifrar_id(cit_cliente_id_hasheado)
    if cit_cliente_id is None:
        raise CitasNotValidParamError("El ID del cliente no es válido")
    return get_cit_cliente(db, cit_cliente_id)


def get_cit_cliente_from_curp(db: Session, curp: str) -> CitCliente:
    """Consultar un cliente por su CURP"""
    try:
        curp = safe_curp(curp)
    except ValueError as error:
        raise CitasNotValidParamError("La CURP no es válida") from error
    cit_cliente = db.query(CitCliente).filter_by(curp=curp).first()
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def get_cit_cliente_from_email(db: Session, email: str) -> CitCliente:
    """Consultar un cliente por su email"""
    try:
        email = safe_email(email)
    except ValueError as error:
        raise CitasNotValidParamError("El email no es válido") from error
    cit_cliente = db.query(CitCliente).filter_by(email=email).first()
    if cit_cliente is None:
        raise CitasNotExistsError("No existe ese cliente")
    if cit_cliente.estatus != "A":
        raise CitasIsDeletedError("No es activo ese cliente, está eliminado")
    return cit_cliente


def create_cit_cliente(db: Session, cit_cliente: CitCliente) -> CitCliente:
    """Crear un cliente"""

    # Validar nombres, apellido primero, apellido segundo, CURP, email y teléfono
    try:
        nombres = safe_string(cit_cliente.nombres, save_enie=True)
        apellido_primero = safe_string(cit_cliente.apellido_primero, save_enie=True)
        apellido_segundo = safe_string(cit_cliente.apellido_segundo, save_enie=True)
        curp = safe_curp(cit_cliente.curp)
        email = safe_email(cit_cliente.email)
        telefono = safe_telefono(cit_cliente.telefono)
    except ValueError as error:
        raise CitasNotValidParamError(f"Los datos no son válidos: {str(error)}") from error

    # Buscar cliente por CURP
    cit_cliente = None
    si_existe = False
    try:
        cit_cliente = get_cit_cliente_from_curp(db, curp)
        si_existe = True
    except CitasNotExistsError:
        try:
            cit_cliente = get_cit_cliente_from_email(db, email)
            si_existe = True
        except CitasNotExistsError:
            pass

    # Si no se encontró, crear el cliente
    if not si_existe:
        renovacion_fecha = datetime.now() + timedelta(days=60)
        cit_cliente = CitCliente(
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            telefono=telefono,
            email=email,
            contrasena_md5="",
            contrasena_sha256="",
            renovacion=renovacion_fecha.date(),
            limite_citas_pendientes=LIMITE_CITAS_PENDIENTES,
        )
        db.add(cit_cliente)
        db.commit()
        db.refresh(cit_cliente)
        si_existe = True

    # Entregar
    return cit_cliente
