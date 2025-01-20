"""
Encuestas Sistemas V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.enc_sistemas import get_enc_sistema_url, update_enc_sistema, validate_enc_sistema
from ...dependencies.database import get_db
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.enc_sistemas import EncSistemaIn, EncSistemaOut, EncSistemaURLOut

enc_sistemas_v2 = APIRouter(prefix="/v2/enc_sistemas", tags=["encuestas"])


@enc_sistemas_v2.get("/validar", response_model=EncSistemaOut)
async def encuesta_sistema_validar(
    hashid: str = None,
    db: Session = Depends(get_db),
):
    """Validar el ID hasheado para ofrecer o negar (provocando una excepcion) el formulario"""
    if not isinstance(hashid, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        enc_servicio = validate_enc_sistema(db, hashid)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncSistemaOut.from_orm(enc_servicio)


@enc_sistemas_v2.post("/contestar", response_model=EncSistemaOut)
async def encuesta_sistema_contestar(
    encuesta: EncSistemaIn,
    db: Session = Depends(get_db),
):
    """Viene el formulario con la Encuesta de Sistemas"""
    try:
        enc_servicio = update_enc_sistema(db, encuesta)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncSistemaOut.from_orm(enc_servicio)


@enc_sistemas_v2.get("/pendiente", response_model=EncSistemaURLOut)
async def encuesta_servicio_pendiente(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Devuelve la URL de la encuesta de servicio PENDIENTE en caso de existir"""
    try:
        url = get_enc_sistema_url(db, current_user.id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    if url is None:
        return EncSistemaURLOut(url="")
    return EncSistemaURLOut(url=url)
