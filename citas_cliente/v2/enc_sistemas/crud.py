"""
Encuestas Sistemas V2, CRUD (create, read, update, and delete)
"""
from sqlalchemy.orm import Session

from .models import EncSistema
from .schemas import EncSistemaIn


def validate_enc_sistema(db: Session, hashid: str) -> EncSistema:
    """Validar la encuesta de servicio por su id haseado"""

    # Validar hashid, si no es valido causa excepcion
    enc_sistema_id = EncSistema.decode_id(hashid)
    if enc_sistema_id is None:
        raise IndexError("No se pudo descifrar el ID de la encuesta de servicio")

    # Consultar, si no se encuentra causa excepcion
    enc_sistema = db.query(EncSistema).get(enc_sistema_id)
    if enc_sistema is None:
        raise IndexError("No existe la encuesta de servicio con el ID dado")

    # Si ya esta eliminado causa excepcion
    if enc_sistema.estatus != "A":
        raise IndexError("No es activa esa encuesta de servicio, fue eliminada")

    # Si el estado no es PENDIENTE causa excepcion
    if enc_sistema.estado != "PENDIENTE":
        raise IndexError("No esta pendiente esa encuesta de servicio")

    # Entregar
    return enc_sistema


def update_enc_sistema(db: Session, encuesta: EncSistemaIn) -> EncSistema:
    """Actualizar la encuesta de servicio con las respuestas y cambiando el estado"""

    # Validar
    enc_sistema = validate_enc_sistema(db, encuesta.hashid)

    # Actualizar
    enc_sistema.respuesta_01 = encuesta.respuesta_01
    enc_sistema.respuesta_02 = encuesta.respuesta_02
    enc_sistema.respuesta_03 = encuesta.respuesta_03
    enc_sistema.estado = "CONTESTADA"
    db.add(enc_sistema)
    db.commit()
    db.refresh(enc_sistema)

    # Entregar
    return enc_sistema
