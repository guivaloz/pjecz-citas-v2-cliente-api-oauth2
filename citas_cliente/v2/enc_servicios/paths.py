"""
Encuestas Servicios V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import validate_enc_servicio, update_enc_servicio
from .schemas import EncServicioIn, EncServicioOut

enc_servicios = APIRouter(prefix="/v2/enc_servicios", tags=["encuestas_servicios"])


@enc_servicios.get("/validar", response_model=EncServicioOut)
async def recuperar_contrasena_validar(
    hashid: str = None,
    db: Session = Depends(get_db),
):
    """Validar la Encuesta de Servicios, validar el ID hasheado para ofrecer o negar el formulario"""
    if not isinstance(hashid, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        enc_servicio = validate_enc_servicio(db, hashid)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)


@enc_servicios.post("/concluir", response_model=EncServicioOut)
async def recuperar_contrasena_concluir(
    encuesta: EncServicioIn,
    db: Session = Depends(get_db),
):
    """Viene el formulario con la Encuesta de Servicios"""
    try:
        enc_servicio = update_enc_servicio(db, encuesta)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return EncServicioOut.from_orm(enc_servicio)
