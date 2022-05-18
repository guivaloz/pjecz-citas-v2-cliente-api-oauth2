"""
Cit Clientes Recuperaciones V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from lib.pwgen import generar_aleatorio

from .models import CitClienteRecuperacion
from .schemas import CitClienteRecuperacionIn, CitClienteRecuperacionConcluirIn
from ..cit_clientes.crud import get_cit_cliente_from_email

EXPIRACION_HORAS = 48


def solicitar_recuperar_contrasena(db: Session, recuperacion: CitClienteRecuperacionIn) -> CitClienteRecuperacion:
    """Solicitar la recuperacion de la contrasena"""

    # Consultar Cliente (tambien valida el correo electronico)
    cit_cliente = get_cit_cliente_from_email(db, recuperacion.email)

    # Consultar si existe una recuperacion para ese cliente
    posible_cit_cliente_recuperacion = db.query(CitClienteRecuperacion).filter_by(cit_cliente_id=cit_cliente.id).first()
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
    return cit_cliente_recuperacion


def validar_recuperar_contrasena(db: Session, hashid: str, cadena_validar: str) -> CitClienteRecuperacion:
    """Validar la recuperacion de la contrasena"""

    # Validar hashid, si no es valido causa excepcion

    # Consultar, si no se encuentra causa excepcion
    cit_cliente_recuperacion_id = None
    cit_cliente_recuperacion = db.query(CitClienteRecuperacion).get(cit_cliente_recuperacion_id)

    # Si ya esta eliminado causa excepcion

    # Si ya se recupero causa excepcion

    # Entregar
    return cit_cliente_recuperacion


def concluir_recuperar_contrasena(db: Session, recuperacion: CitClienteRecuperacionConcluirIn) -> CitClienteRecuperacion:
    """Concluir la recuperacion de la contrasena"""

    # Ejecutar la funcion que nos apoya con la validacion
    cit_cliente_recuperacion = validar_recuperar_contrasena(db, recuperacion.hashid, recuperacion.cadena_validar)

    # Actualizar el cliente con la nueva contrasena

    # Actualizar la recuperacion con ya_recuperado en verdadero

    # Entregar
    return cit_cliente_recuperacion
