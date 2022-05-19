"""
Cit Clientes Recuperaciones V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import solicitar_recuperar_contrasena, validar_recuperar_contrasena, concluir_recuperar_contrasena
from .schemas import CitClienteRecuperacionIn, CitClienteRecuperacionOut, CitClienteRecuperacionValidarOut, CitClienteRecuperacionConcluirIn, CitClienteRecuperacionConcluirOut

cit_clientes_recuperaciones = APIRouter(prefix="/v2/recuperar_contrasena", tags=["recuperar contrasena"])


@cit_clientes_recuperaciones.post("/solicitar", response_model=CitClienteRecuperacionOut)
async def recuperar_contrasena_solicitar(
    recuperacion: CitClienteRecuperacionIn,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, recibo el formulario con mi correo electronico"""
    try:
        cit_cliente_recuperacion = solicitar_recuperar_contrasena(db, recuperacion)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion)


@cit_clientes_recuperaciones.get("/validar", response_model=CitClienteRecuperacionValidarOut)
async def recuperar_contrasena_validar(
    hashid: str = None,
    cadena_validar: str = None,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, viene del URL proporcionado, entrego el formulario para cambiarla"""
    if not isinstance(hashid, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if not isinstance(cadena_validar, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        cit_cliente_recuperacion = validar_recuperar_contrasena(db, hashid, cadena_validar)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionValidarOut.from_orm(cit_cliente_recuperacion)


@cit_clientes_recuperaciones.post("/concluir", response_model=CitClienteRecuperacionConcluirOut)
async def recuperar_contrasena_concluir(
    recuperacion: CitClienteRecuperacionConcluirIn,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, recibo el formulario para cambiarla"""
    try:
        cit_cliente_recuperacion = concluir_recuperar_contrasena(db, recuperacion)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionConcluirOut.from_orm(cit_cliente_recuperacion)
