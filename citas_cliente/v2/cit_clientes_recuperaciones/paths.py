"""
Cit Clientes Recuperaciones V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import post_cit_cliente_recuperacion
from .schemas import CitClienteRecuperacionIn, CitClienteRecuperacionOut

cit_clientes_recuperaciones = APIRouter(prefix="/v2/cit_clientes_recuperaciones", tags=["clientes"])


@cit_clientes_recuperaciones.post("", response_model=CitClienteRecuperacionOut)
async def recuperar_cuenta(
    recuperacion: CitClienteRecuperacionIn,
    db: Session = Depends(get_db),
):
    """Recibe el formulario (con el correo electronico) para recuperar cuenta porque olvido su contrasena"""
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


@cit_clientes_recuperaciones.get("/<cadena_validar:str>", response_model=CitClienteRecuperacionOut)
async def recuperar_cuenta_cargar(
    cadena_validar: str,
    db: Session = Depends(get_db),
):
    """Al dar clic en el URL se recibe la cadena_validar y se pide que defina su contrasena"""


@cit_clientes_recuperaciones.post("/<cadena_validar:str>", response_model=CitClienteRecuperacionOut)
async def recuperar_cuenta_entregar(
    cadena_validar: str,
    db: Session = Depends(get_db),
):
    """Recibe el formulario con la cadena_validar y la nueva contrasena"""
