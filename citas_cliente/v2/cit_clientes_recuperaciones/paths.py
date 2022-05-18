"""
Cit Clientes Recuperaciones V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import post_cit_cliente_recuperacion
from .schemas import CitClienteRecuperacionIn, CitClienteRecuperacionOut, CitClienteRecuperacionValidarOut, CitClienteRecuperacionConcluirIn, CitClienteRecuperacionConcluirOut

cit_clientes_recuperaciones = APIRouter(prefix="/v2/recuperar_contrasena", tags=["recuperar contrasena"])


@cit_clientes_recuperaciones.post("/solicitar", response_model=CitClienteRecuperacionOut)
async def solicitar_recuperar_contrasena(
    recuperacion: CitClienteRecuperacionIn,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, recibo el formulario con mi correo electronico"""
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


@cit_clientes_recuperaciones.get("/validar/<hashid:str>/<cadena_validar:str>", response_model=CitClienteRecuperacionValidarOut)
async def validar_recuperar_contrasena(
    hashid: str,
    cadena_validar: str,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, viene del URL proporcionado, entrego el formulario para cambiarla"""


@cit_clientes_recuperaciones.post("/concluir", response_model=CitClienteRecuperacionConcluirOut)
async def concluir_recuperar_contrasena(
    recuperacion: CitClienteRecuperacionConcluirIn,
    db: Session = Depends(get_db),
):
    """Recibe el formulario con la cadena_validar y la nueva contrasena"""
