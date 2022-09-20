"""
Encuestas Sistemas V2, CRUD (create, read, update, and delete)
"""
from typing import Optional

from sqlalchemy.orm import Session
from hashids import Hashids

from config.settings import POLL_SYSTEM_URL, SALT
from lib.safe_string import safe_string

from .models import EncSistema
from .schemas import EncSistemaIn


def validate_enc_sistema(db: Session, hashid: str) -> EncSistema:
    """Validar la encuesta de servicio por su id haseado"""

    # Validar hashid, si no es valido causa excepcion
    enc_sistema_id = EncSistema.decode_id(hashid)
    if enc_sistema_id is None:
        raise IndexError("No se pudo descifrar el ID de la encuesta")

    # Consultar, si no se encuentra causa excepcion
    enc_sistema = db.query(EncSistema).get(enc_sistema_id)
    if enc_sistema is None:
        raise IndexError("No existe la encuesta con el ID dado")

    # Si ya esta eliminado causa excepcion
    if enc_sistema.estatus != "A":
        raise IndexError("No es activa esa encuesta, fue eliminada")

    # Si el estado no es PENDIENTE causa excepcion
    if enc_sistema.estado != "PENDIENTE":
        raise IndexError("La encuesta ya fue contestada o cancelada")

    # Entregar
    return enc_sistema


def update_enc_sistema(db: Session, encuesta: EncSistemaIn) -> EncSistema:
    """Actualizar la encuesta de servicio con las respuestas y cambiando el estado"""

    # Validar
    enc_sistema = validate_enc_sistema(db, encuesta.hashid)

    # Respuesta 1 es entero de 1 a 5
    if encuesta.respuesta_01 < 1 or encuesta.respuesta_01 > 5:
        raise ValueError("El valor de la respuesta 1 esta fuera del rango")
    enc_sistema.respuesta_01 = encuesta.respuesta_01

    # Respuesta 2 es texto
    enc_sistema.respuesta_02 = safe_string(encuesta.respuesta_02)

    # Respuesta 3 es texto
    enc_sistema.respuesta_03 = safe_string(encuesta.respuesta_03)

    # Cambiar el estado
    enc_sistema.estado = "CONTESTADO"

    # Actualizar
    db.add(enc_sistema)
    db.commit()
    db.refresh(enc_sistema)

    # Entregar
    return enc_sistema


def get_enc_sistema_url(db: Session, cit_cliente_id: int) -> Optional[str]:
    """Obtener la URL de la encuesta de sistemas del cliente si existe"""

    # Consultar la encuesta de sistemas PENDIENTE
    enc_sistema = db.query(EncSistema).filter(EncSistema.cit_cliente_id == cit_cliente_id).filter(EncSistema.estado == "PENDIENTE").first()

    # Si no existe, entregar None
    if enc_sistema is None:
        return None

    # Preparar el cifrado
    hashids = Hashids(SALT, min_length=8)

    # Entregar la URL
    return f"{POLL_SYSTEM_URL}?hashid={hashids.encode(enc_sistema.id)}"
