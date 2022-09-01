"""
Encuestas Sistemas V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import validate_enc_sistema, update_enc_sistema
from .schemas import EncSistemaIn, EncSistemaOut

enc_sistemas = APIRouter(prefix="/v2/enc_sistemas", tags=["encuestas"])


@enc_sistemas.get("/validar", response_model=EncSistemaOut)
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


@enc_sistemas.post("/contestar", response_model=EncSistemaOut)
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
