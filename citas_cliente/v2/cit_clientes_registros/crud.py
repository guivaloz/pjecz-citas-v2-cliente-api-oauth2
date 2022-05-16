"""
Cit Clientes Registros V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
import re
from sqlalchemy.orm import Session

from lib.pwgen import generar_aleatorio
from lib.safe_string import safe_string, CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP

from .models import CitClienteRegistro
from .schemas import CitClienteRegistroIn
from ..cit_clientes.crud import get_cit_cliente_from_curp, get_cit_cliente_from_email

EXPIRACION_HORAS = 48


def post_cit_cliente_registro(db: Session, registro: CitClienteRegistroIn) -> CitClienteRegistro:
    """Recibir los datos para el registro de un nuevo cliente"""

    # Asegurarse que los datos de entrada son correctos
    nombres = safe_string(registro.nombres)
    apellido_primero = safe_string(registro.apellido_primero)
    apellido_segundo = safe_string(registro.apellido_segundo)
    curp = safe_string(registro.curp)
    email = registro.email.strip().lower()
    telefono = registro.telefono.strip()

    # Validar CURP
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP no es valido")

    # Validar email
    if re.match(EMAIL_REGEXP, email) is None:
        raise ValueError("El correo electronico no es valido")

    # Validar telefono
    if re.match(TELEFONO_REGEXP, telefono) is None:
        raise ValueError("El telefono no es valido")

    # Verificar que no exista un cliente con ese correo electronico o CURP
    try:
        posible_cit_cliente_con_email = get_cit_cliente_from_email(db, email)
        if posible_cit_cliente_con_email is not None:
            raise IndexError("Ya existe un cliente con ese correo electronico.")
        posible_cit_cliente_con_curp = get_cit_cliente_from_curp(db, curp)
        if posible_cit_cliente_con_curp is not None:
            raise IndexError("Ya existe una cuenta con ese CURP.")
    except IndexError:
        pass
    except ValueError as error:
        raise error

    # Verificar que no haya un registro pendiente con ese correo electronico
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(email=email).filter_by(ya_registrado=False).first()
    )
    if posible_cit_cliente_registro is not None:
        raise IndexError("Ya hay una solicitud de registro para ese correo electronico.")

    # Verificar que no haya un registro pendiente con ese CURP
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(curp=curp).filter_by(ya_registrado=False).first()
    )
    if posible_cit_cliente_registro is not None:
        raise IndexError("Ya hay una solicitud de registro para ese CURP.")

    # Insertar registro
    cit_cliente_registro = CitClienteRegistro(
        nombres=nombres,
        apellido_primero=apellido_primero,
        apellido_segundo=apellido_segundo,
        curp=curp,
        telefono=telefono,
        email=email,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_aleatorio(largo=24),
        ya_registrado=False,
    )
    db.add(cit_cliente_registro)
    db.commit()
    db.refresh(cit_cliente_registro)
    return cit_cliente_registro
