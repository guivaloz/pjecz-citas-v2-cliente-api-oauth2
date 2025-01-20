"""
Encuestas Servicios V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.enc_servicios import get_enc_servicio_url, update_enc_servicio, validate_enc_servicio
from ...dependencies.database import get_db
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.enc_servicios import EncServicioIn, EncServicioOut, EncServicioURLOut

enc_servicios_v2 = APIRouter(prefix="/v2/enc_servicios", tags=["encuestas"])


@enc_servicios_v2.get("/validar", response_model=EncServicioOut)
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


@enc_servicios_v2.post("/contestar", response_model=EncServicioOut)
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


@enc_servicios_v2.get("/pendiente", response_model=EncServicioURLOut)
async def encuesta_servicio_pendiente(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Devuelve la URL de la encuesta de servicio PENDIENTE en caso de existir"""
    try:
        url = get_enc_servicio_url(db, current_user.id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    if url is None:
        return EncServicioURLOut(url="")
    return EncServicioURLOut(url=url)
