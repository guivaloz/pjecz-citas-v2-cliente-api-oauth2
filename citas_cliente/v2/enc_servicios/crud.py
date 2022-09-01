"""
Encuestas Servicios V2, CRUD (create, read, update, and delete)
"""
from sqlalchemy.orm import Session

from lib.safe_string import safe_string

from .models import EncServicio
from .schemas import EncServicioIn


def validate_enc_servicio(db: Session, hashid: str) -> EncServicio:
    """Validar la encuesta de servicio por su id haseado"""

    # Validar hashid, si no es valido causa excepcion
    enc_servicio_id = EncServicio.decode_id(hashid)
    if enc_servicio_id is None:
        raise IndexError("No se pudo descifrar el ID de la encuesta de servicio")

    # Consultar, si no se encuentra causa excepcion
    enc_servicio = db.query(EncServicio).get(enc_servicio_id)
    if enc_servicio is None:
        raise IndexError("No existe la encuesta de servicio con el ID dado")

    # Si ya esta eliminado causa excepcion
    if enc_servicio.estatus != "A":
        raise IndexError("No es activa esa encuesta de servicio, fue eliminada")

    # Si el estado no es PENDIENTE causa excepcion
    if enc_servicio.estado != "PENDIENTE":
        raise IndexError("No esta pendiente esa encuesta de servicio")

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
    enc_servicio.respuesta_04 = safe_string(encuesta.respuesta_04)

    # Cambiar el estado a Contestada
    enc_servicio.estado = "CONTESTADA"

    # Actualizar
    db.add(enc_servicio)
    db.commit()
    db.refresh(enc_servicio)

    # Entregar
    return enc_servicio
