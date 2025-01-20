"""
Cit Clientes Registros V2, CRUD (create, read, update, and delete)
"""

import re
from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...dependencies.pwgen import generar_aleatorio
from ...dependencies.redis import task_queue
from ...dependencies.safe_string import CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP, safe_string
from ...models.cit_clientes_registros import CitClienteRegistro
from ...schemas.v2.cit_clientes_registros import CitClienteRegistroConcluirIn, CitClienteRegistroIn
from ...settings import LIMITE_CITAS_PENDIENTES
from .cit_clientes import CitCliente

EXPIRACION_HORAS = 48


def request_new_account(db: Session, registro: CitClienteRegistroIn) -> CitClienteRegistro:
    """Solicitar la creacion de una nueva cuenta"""

    # Procesar datos de entrada con las funciones 'safe'
    nombres = safe_string(registro.nombres, save_enie=True)
    apellido_primero = safe_string(registro.apellido_primero, save_enie=True)
    apellido_segundo = safe_string(registro.apellido_segundo, save_enie=True)
    curp = safe_string(registro.curp)
    email = registro.email.strip().lower()
    telefono = registro.telefono.strip()

    # Validar nombres
    if nombres == "":
        raise ValueError("El nombre no es valido")

    # Validar apellido primero
    if apellido_primero == "":
        raise ValueError("El apellido primero no es valido")

    # Validar apellido segundo
    if apellido_segundo == "":
        raise ValueError("El apellido segundo no es valido")

    # Validar CURP
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP no es valido")

    # Validar email
    if re.match(EMAIL_REGEXP, email) is None:
        raise ValueError("El correo electronico no es valido")

    # Validar telefono
    if re.match(TELEFONO_REGEXP, telefono) is None:
        raise ValueError("El telefono no es valido")

    # Verificar que no exista un cliente con ese CURP
    posible_cit_cliente_con_curp = db.query(CitCliente).filter_by(curp=curp).first()
    if posible_cit_cliente_con_curp is not None:
        raise ValueError("No puede registrarse porque ya una cuenta con ese CURP.")

    # Verificar que no exista un cliente con ese correo electronico
    posible_cit_cliente_con_email = db.query(CitCliente).filter_by(email=email).first()
    if posible_cit_cliente_con_email is not None:
        raise ValueError("No puede registrarse porque ya una cuenta con ese correo electrónico.")

    # Verificar que no haya un registro pendiente con ese correo electronico
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(email=email).filter_by(ya_registrado=False).filter_by(estatus="A").first()
    )
    if posible_cit_cliente_registro is not None:
        raise ValueError("Ya hay una solicitud de registro para ese correo electronico.")

    # Verificar que no haya un registro pendiente con ese CURP
    posible_cit_cliente_registro = (
        db.query(CitClienteRegistro).filter_by(curp=curp).filter_by(ya_registrado=False).filter_by(estatus="A").first()
    )
    if posible_cit_cliente_registro is not None:
        raise ValueError("Ya hay una solicitud de registro para ese CURP.")

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

    # Agregar tarea en el fondo para que se envie un mensaje via correo electronico
    task_queue.enqueue(
        "citas_admin.blueprints.cit_clientes_registros.tasks.enviar",
        cit_cliente_registro_id=cit_cliente_registro.id,
    )

    # Entregar
    return cit_cliente_registro


def validate_new_account(db: Session, hashid: str, cadena_validar: str) -> CitClienteRegistro:
    """Validar la recuperacion de la contrasena"""

    # Validar hashid, si no es valido causa excepcion
    cit_cliente_registro_id = CitClienteRegistro.decode_id(hashid)
    if cit_cliente_registro_id is None:
        raise IndexError("No se pudo descifrar el ID")

    # Consultar, si no se encuentra causa excepcion
    cit_cliente_registro = db.query(CitClienteRegistro).get(cit_cliente_registro_id)
    if cit_cliente_registro is None:
        raise IndexError("No existe la solicitud de nueva cuenta con el ID dado")

    # Si ya esta eliminado causa excepcion
    if cit_cliente_registro.estatus != "A":
        raise IndexError("No es activa esa solicitud de nueva cuenta, fue eliminada")

    # Si ya se recupero causa excepcion
    if cit_cliente_registro.ya_registrado is True:
        raise IndexError("No se puede registrar esta cuenta porque ya fue hecha")

    # Comparar la cadena de validacion
    if cit_cliente_registro.cadena_validar != cadena_validar:
        raise IndexError("No es igual la cadena de validacion")

    # Entregar
    return cit_cliente_registro


def terminate_new_account(db: Session, registro: CitClienteRegistroConcluirIn) -> CitClienteRegistro:
    """Concluir la recuperacion de la contrasena"""

    # Ejecutar la funcion que nos apoya con la validacion
    cit_cliente_registro = validate_new_account(db, registro.hashid, registro.cadena_validar)

    # Definir la fecha de renovación dos meses después
    renovacion_fecha = datetime.now() + timedelta(days=60)

    # Cifrar la contrasena
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")

    # Insertar el nuevo cliente
    cit_cliente = CitCliente(
        nombres=cit_cliente_registro.nombres,
        apellido_primero=cit_cliente_registro.apellido_primero,
        apellido_segundo=cit_cliente_registro.apellido_segundo,
        curp=cit_cliente_registro.curp,
        telefono=cit_cliente_registro.telefono,
        email=cit_cliente_registro.email,
        contrasena_md5="",
        contrasena_sha256=pwd_context.hash(registro.password),
        renovacion=renovacion_fecha.date(),
        limite_citas_pendientes=LIMITE_CITAS_PENDIENTES,
    )
    db.add(cit_cliente)

    # Actualizar con ya_registrado en verdadero
    cit_cliente_registro.ya_registrado = True
    db.add(cit_cliente_registro)
    db.commit()
    db.refresh(cit_cliente_registro)

    # Entregar
    return cit_cliente_registro
