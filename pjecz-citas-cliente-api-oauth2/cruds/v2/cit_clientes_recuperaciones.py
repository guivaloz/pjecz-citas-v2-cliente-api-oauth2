"""
Cit Clientes Recuperaciones V2, CRUD (create, read, update, and delete)
"""

from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...dependencies.pwgen import generar_aleatorio
from ...dependencies.redis import task_queue
from ...models.cit_clientes_recuperaciones import CitClienteRecuperacion
from ...schemas.v2.cit_clientes_recuperaciones import CitClienteRecuperacionConcluirIn, CitClienteRecuperacionIn
from .cit_clientes import get_cit_cliente, get_cit_cliente_from_email

EXPIRACION_HORAS = 48


def request_recover_password(db: Session, recuperacion: CitClienteRecuperacionIn) -> CitClienteRecuperacion:
    """Solicitar la recuperacion de la contrasena"""

    # Consultar Cliente (tambien valida el correo electronico)
    cit_cliente = get_cit_cliente_from_email(db, recuperacion.email)

    # Consultar si existe una recuperacion para ese cliente
    posible_cit_cliente_recuperacion = (
        db.query(CitClienteRecuperacion)
        .filter_by(cit_cliente_id=cit_cliente.id)
        .filter_by(ya_recuperado=False)
        .filter_by(estatus="A")
        .first()
    )
    if posible_cit_cliente_recuperacion is not None:
        raise ValueError("Ya existe una recuperacion para ese email.")

    # Insertar recuperacion
    cit_cliente_recuperacion = CitClienteRecuperacion(
        cit_cliente=cit_cliente,
        expiracion=datetime.now() + timedelta(hours=EXPIRACION_HORAS),
        cadena_validar=generar_aleatorio(largo=24),
        ya_recuperado=False,
    )
    db.add(cit_cliente_recuperacion)
    db.commit()
    db.refresh(cit_cliente_recuperacion)

    # Agregar tarea en el fondo para que se envie un mensaje via correo electronico
    task_queue.enqueue(
        "citas_admin.blueprints.cit_clientes_recuperaciones.tasks.enviar",
        cit_cliente_recuperacion_id=cit_cliente_recuperacion.id,
    )

    # Entregar
    return cit_cliente_recuperacion


def validate_recover_password(db: Session, hashid: str, cadena_validar: str) -> CitClienteRecuperacion:
    """Validar la recuperacion de la contrasena"""

    # Validar hashid, si no es valido causa excepcion
    cit_cliente_recuperacion_id = CitClienteRecuperacion.decode_id(hashid)
    if cit_cliente_recuperacion_id is None:
        raise IndexError("No se pudo descifrar el ID")

    # Consultar, si no se encuentra causa excepcion
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)
    if cit_cliente_recuperacion is None:
        raise IndexError("No existe la recuperacion con el ID dado")

    # Si ya esta eliminado causa excepcion
    if cit_cliente_recuperacion.estatus != "A":
        raise IndexError("No es activa esa recuperacion, fue eliminada")

    # Si ya se recupero causa excepcion
    if cit_cliente_recuperacion.ya_recuperado is True:
        raise IndexError("No se puede recuperar esta contrasena porque ya fue recuperada")

    # Comparar la cadena de validacion
    if cit_cliente_recuperacion.cadena_validar != cadena_validar:
        raise IndexError("No es igual la cadena de validacion")

    # Entregar
    return cit_cliente_recuperacion


def terminate_recover_password(db: Session, recuperacion: CitClienteRecuperacionConcluirIn) -> CitClienteRecuperacion:
    """Concluir la recuperacion de la contrasena"""

    # Validar la recuperacion
    cit_cliente_recuperacion = validate_recover_password(db, recuperacion.hashid, recuperacion.cadena_validar)

    # Definir la fecha de renovación dos meses después
    renovacion_fecha = datetime.now() + timedelta(days=60)

    # Cifrar la contrasena
    pwd_context = CryptContext(schemes=["pbkdf2_sha256", "des_crypt"], deprecated="auto")

    # Actualizar el cliente con la nueva contrasena
    cit_cliente = get_cit_cliente(db, cit_cliente_recuperacion.cit_cliente_id)
    cit_cliente.contrasena_md5 = ""
    cit_cliente.contrasena_sha256 = pwd_context.hash(recuperacion.password)
    cit_cliente.renovacion = renovacion_fecha.date()
    db.add(cit_cliente)

    # Actualizar con ya_recuperado en verdadero
    cit_cliente_recuperacion.ya_recuperado = True
    db.add(cit_cliente_recuperacion)
    db.commit()
    db.refresh(cit_cliente_recuperacion)

    # Entregar
    return cit_cliente_recuperacion
