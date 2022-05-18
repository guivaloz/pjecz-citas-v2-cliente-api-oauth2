"""
Cit Clientes Registros V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
import re
from sqlalchemy.orm import Session

from lib.pwgen import generar_aleatorio
from lib.safe_string import safe_string, CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP

from .models import CitClienteRegistro
from .schemas import CitClienteRegistroIn, CitClienteRegistroConcluirIn
from ..cit_clientes.crud import get_cit_cliente_from_curp, get_cit_cliente_from_email

EXPIRACION_HORAS = 48


def solicitar_nueva_cuenta(db: Session, registro: CitClienteRegistroIn) -> CitClienteRegistro:
    """Solicitar la creacion de una nueva cuenta"""

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
    posible_cit_cliente_registro = db.query(CitClienteRegistro).filter_by(email=email).filter_by(ya_registrado=False).first()
    if posible_cit_cliente_registro is not None:
        raise IndexError("Ya hay una solicitud de registro para ese correo electronico.")

    # Verificar que no haya un registro pendiente con ese CURP
    posible_cit_cliente_registro = db.query(CitClienteRegistro).filter_by(curp=curp).filter_by(ya_registrado=False).first()
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


def validar_nueva_cuenta(db: Session, hashid: str, cadena_validar: str) -> CitClienteRegistro:
    """Validar la recuperacion de la contrasena"""

    # Validar hashid, si no es valido causa excepcion

    # Consultar, si no se encuentra causa excepcion
    cit_cliente_registro_id = None
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)

    # Si ya esta eliminado causa excepcion

    # Si ya se recupero causa excepcion

    # Entregar
    return cit_cliente_registro


def concluir_nueva_cuenta(db: Session, registro: CitClienteRegistroConcluirIn) -> CitClienteRegistro:
    """Concluir la recuperacion de la contrasena"""

    # Ejecutar la funcion que nos apoya con la validacion
    cit_cliente_registro = validar_nueva_cuenta(db, registro.hashid, registro.cadena_validar)

    # Actualizar el cliente con la nueva contrasena

    # Actualizar la recuperacion con ya_recuperado en verdadero

    # Entregar
    return cit_cliente_registro
