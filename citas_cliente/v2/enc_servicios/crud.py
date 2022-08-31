"""
Encuestas Servicios V2, CRUD (create, read, update, and delete)
"""
from sqlalchemy.orm import Session

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

    # Actualizar
    enc_servicio.respuesta_01 = encuesta.respuesta_01
    enc_servicio.respuesta_02 = encuesta.respuesta_02
    enc_servicio.respuesta_03 = encuesta.respuesta_03
    enc_servicio.respuesta_04 = encuesta.respuesta_04
    enc_servicio.estado = "CONTESTADA"
    db.add(enc_servicio)
    db.commit()
    db.refresh(enc_servicio)

    # Entregar
    return enc_servicio
