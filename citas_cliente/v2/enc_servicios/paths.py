"""
Encuestas Servicios V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from .crud import validate_enc_servicio, update_enc_servicio, get_enc_servicio
from .schemas import EncServicioIn, EncServicioOut

enc_servicios = APIRouter(prefix="/v2/enc_servicios", tags=["encuestas"])


@enc_servicios.get("/validar", response_model=EncServicioOut)
async def encuesta_servicio_validar(
    hashid: str = None,
    db: Session = Depends(get_db),
):
    """Validar el ID hasheado para ofrecer o negar (provocando una excepcion) el formulario"""
    if not isinstance(hashid, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        enc_servicio = validate_enc_servicio(db, hashid)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)


@enc_servicios.post("/contestar", response_model=EncServicioOut)
async def encuesta_servicio_contestar(
    encuesta: EncServicioIn,
    db: Session = Depends(get_db),
):
    """Viene el formulario con la Encuesta de Servicio"""
    try:
        enc_servicio = update_enc_servicio(db, encuesta)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)


@enc_servicios.get("/pendiente", response_model=EncServicioOut)
async def encuesta_servicio_pendiente(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Devuelve la encuesta de servicio pendiente de existir"""
    try:
        enc_servicio = get_enc_servicio(db, current_user.id)
        if enc_servicio is None:
            return EncServicioOut()
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)
