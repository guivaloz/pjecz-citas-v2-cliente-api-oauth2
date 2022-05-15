"""
Cit Clientes Registros v1, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from lib.pwgen import generar_aleatorio

from .models import CitClienteRegistro
from .schemas import CitClienteRegistroIn
from ..cit_clientes.crud import get_cit_cliente_from_curp, get_cit_cliente_from_email

EXPIRACION_HORAS = 48


def post_cit_cliente_registro(db: Session, registro: CitClienteRegistroIn) -> CitClienteRegistro:
    """Recibir los datos para el registro de un nuevo cliente"""

    # Verificar que no exista un cliente con ese correo electronico
    posible_cit_cliente = get_cit_cliente_from_email(db, registro.email)
    if posible_cit_cliente is not None:
        raise ValueError("Ya existe un cliente con ese correo electronico.")

    # Verificar que no exista un cliente con ese CURP
    posible_cit_cliente = get_cit_cliente_from_curp(db, registro.curp)
    if posible_cit_cliente is not None:
        raise ValueError("Ya existe una cuenta con ese CURP.")

    # Verificar que no haya un registro pendiente con ese correo electronico
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(email=registro.email).filter_by(ya_registrado=False).first()
    )
    if posible_cit_cliente_registro is not None:
        raise ValueError("Ya hay una solicitud de registro para ese correo electronico.")

    # Verificar que no haya un registro pendiente con ese CURP
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(curp=registro.curp).filter_by(ya_registrado=False).first()
    )
    if posible_cit_cliente_registro is not None:
        raise ValueError("Ya hay una solicitud de registro para ese CURP.")

    # Insertar registro
    cit_cliente_registro = CitClienteRegistro(
        nombres=registro.nombres,
        apellido_primero=registro.apellido_primero,
        apellido_segundo=registro.apellido_segundo,
        curp=registro.curp,
        telefono=registro.telefono,
        email=registro.email,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_aleatorio(largo=24),
        ya_registrado=False,
    )
    db.add(cit_cliente_registro)
    db.commit()
    db.refresh(cit_cliente_registro)
    return cit_cliente_registro
