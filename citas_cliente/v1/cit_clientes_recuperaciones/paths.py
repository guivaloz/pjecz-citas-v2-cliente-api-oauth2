"""
Cit Clientes Recuperaciones v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import post_cit_cliente_recuperacion
from .schemas import CitClienteRecuperacionIn, CitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/v1/cit_clientes_recuperaciones", tags=["clientes"])


@cit_clientes_recuperaciones.post("", response_model=CitClienteRecuperacionOut)
async def recuperar_contrasena(
    recuperacion: CitClienteRecuperacionIn,
    db: Session = Depends(get_db),
):
    """Recuperar contrasena"""
    try:
        cit_cliente_recuperacion = post_cit_cliente_recuperacion(db, recuperacion)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionOut(
        email=cit_cliente_recuperacion.cit_cliente.email,
        expiracion=cit_cliente_recuperacion.expiracion,
    )
