"""
Cit Clientes Registros V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
import re
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from lib.pwgen import generar_aleatorio
from lib.safe_string import safe_string, CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP

from .models import CitClienteRegistro
from .schemas import CitClienteRegistroIn, CitClienteRegistroConcluirIn
from ..cit_clientes.models import CitCliente

EXPIRACION_HORAS = 48


def solicitar_nueva_cuenta(db: Session, registro: CitClienteRegistroIn) -> CitClienteRegistro:
    """Solicitar la creacion de una nueva cuenta"""

    # Procesar datos de entrada con las funciones 'safe'
    nombres = safe_string(registro.nombres)
    apellido_primero = safe_string(registro.apellido_primero)
    apellido_segundo = safe_string(registro.apellido_segundo)
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
        if posible_cit_cliente_con_curp.estatus == "A":
            raise IndexError("No puede registrarse porque ya una cuenta con ese CURP.")
        else:
            raise IndexError("No puede registrarse porque hay una cuenta suspendida con ese CURP.")

    # Verificar que no exista un cliente con ese correo electronico
    posible_cit_cliente_con_email = db.query(CitCliente).filter_by(email=email).first()
    if posible_cit_cliente_con_email is not None:
        if posible_cit_cliente_con_curp.estatus == "A":
            raise IndexError("No puede registrarse porque ya una cuenta con ese correo electrónico.")
        else:
            raise IndexError("No puede registrarse porque hay una cuenta suspendida con ese correo electrónico.")

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

    # Entregar
    return cit_cliente_registro


def validar_nueva_cuenta(db: Session, hashid: str, cadena_validar: str) -> CitClienteRegistro:
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


def concluir_nueva_cuenta(db: Session, registro: CitClienteRegistroConcluirIn) -> CitClienteRegistro:
    """Concluir la recuperacion de la contrasena"""

    # Ejecutar la funcion que nos apoya con la validacion
    cit_cliente_registro = validar_nueva_cuenta(db, registro.hashid, registro.cadena_validar)

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
    )
    db.add(cit_cliente)

    # Actualizar con ya_registrado en verdadero
    cit_cliente_registro.ya_registrado = True
    db.add(cit_cliente_registro)
    db.commit()
    db.refresh(cit_cliente_registro)

    # Entregar
    return cit_cliente_registro
