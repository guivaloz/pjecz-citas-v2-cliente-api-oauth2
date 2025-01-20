"""
Encuestas Servicios V2, CRUD (create, read, update, and delete)
"""

from typing import Optional

from hashids import Hashids
from sqlalchemy.orm import Session

from ...dependencies.safe_string import safe_string
from ...models.enc_servicios import EncServicio
from ...schemas.v2.enc_servicios import EncServicioIn
from ...settings import POLL_SERVICE_URL, SALT


def validate_enc_servicio(db: Session, hashid: str) -> EncServicio:
    """Validar la encuesta de servicio por su id haseado"""

    # Validar hashid, si no es valido causa excepcion
    enc_servicio_id = EncServicio.decode_id(hashid)
    if enc_servicio_id is None:
        raise IndexError("No se pudo descifrar el ID de la encuesta")

    # Consultar, si no se encuentra causa excepcion
    enc_servicio = db.query(EncServicio).get(enc_servicio_id)
    if enc_servicio is None:
        raise IndexError("No existe la encuesta con el ID dado")

    # Si ya esta eliminado causa excepcion
    if enc_servicio.estatus != "A":
        raise IndexError("No es activa esa encuesta, fue eliminada")

    # Si el estado no es PENDIENTE causa excepcion
    if enc_servicio.estado != "PENDIENTE":
        raise IndexError("La encuesta ya fue contestada o cancelada")

    # Entregar
    return enc_servicio


def update_enc_servicio(db: Session, encuesta: EncServicioIn) -> EncServicio:
    """Actualizar la encuesta de servicio con las respuestas y cambiando el estado"""

    # Validar
    enc_servicio = validate_enc_servicio(db, encuesta.hashid)

    # Respuesta 1 es entero de 1 a 5
    if encuesta.respuesta_01 < 1 or encuesta.respuesta_01 > 5:
        raise ValueError("El valor de la respuesta 1 esta fuera del rango")
    enc_servicio.respuesta_01 = encuesta.respuesta_01

    # Respuesta 2 es entero de 1 a 5
    if encuesta.respuesta_02 < 1 or encuesta.respuesta_02 > 5:
        raise ValueError("El valor de la respuesta 2 esta fuera del rango")
    enc_servicio.respuesta_02 = encuesta.respuesta_02

    # Respuesta 3 es entero de 1 a 5
    if encuesta.respuesta_03 < 1 or encuesta.respuesta_03 > 5:
        raise ValueError("El valor de la respuesta 3 esta fuera del rango")
    enc_servicio.respuesta_03 = encuesta.respuesta_03

    # Respuesta 4 es un texto
    enc_servicio.respuesta_04 = safe_string(encuesta.respuesta_04, max_len=512)

    # Cambiar el estado
    enc_servicio.estado = "CONTESTADO"

    # Actualizar
    db.add(enc_servicio)
    db.commit()
    db.refresh(enc_servicio)

    # Entregar
    return enc_servicio


def get_enc_servicio_url(db: Session, cit_cliente_id: int) -> Optional[str]:
    """Obtener la URL de la encuesta de servicio del cliente si existe"""

    # Consultar la encuesta de servicio PENDIENTE
    enc_servicio = (
        db.query(EncServicio)
        .filter(EncServicio.cit_cliente_id == cit_cliente_id)
        .filter(EncServicio.estado == "PENDIENTE")
        .first()
    )

    # Si no existe, entregar None
    if enc_servicio is None:
        return None

    # Preparar el cifrado
    hashids = Hashids(SALT, min_length=8)

    # Entregar la URL
    return f"{POLL_SERVICE_URL}?hashid={hashids.encode(enc_servicio.id)}"
