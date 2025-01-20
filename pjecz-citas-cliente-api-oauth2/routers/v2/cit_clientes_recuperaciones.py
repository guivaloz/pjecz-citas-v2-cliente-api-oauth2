"""
Cit Clientes Recuperaciones V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...cruds.v2.cit_clientes_recuperaciones import (
    request_recover_password,
    terminate_recover_password,
    validate_recover_password,
)
from ...dependencies.database import get_db
from ...schemas.v2.cit_clientes_recuperaciones import (
    CitClienteRecuperacionConcluirIn,
    CitClienteRecuperacionConcluirOut,
    CitClienteRecuperacionIn,
    CitClienteRecuperacionOut,
    CitClienteRecuperacionValidarOut,
)

cit_clientes_recuperaciones_v2 = APIRouter(prefix="/v2/recuperar_contrasena", tags=["recuperar contrasena"])


@cit_clientes_recuperaciones_v2.post("/solicitar", response_model=CitClienteRecuperacionOut)
async def recuperar_contrasena_solicitar(
    recuperacion: CitClienteRecuperacionIn,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, recibo el formulario con mi correo electronico"""
    try:
        cit_cliente_recuperacion = request_recover_password(db, recuperacion)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionOut.from_orm(cit_cliente_recuperacion)


@cit_clientes_recuperaciones_v2.get("/validar", response_model=CitClienteRecuperacionValidarOut)
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
        cit_cliente_recuperacion = validate_recover_password(db, hashid, cadena_validar)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionValidarOut.from_orm(cit_cliente_recuperacion)


@cit_clientes_recuperaciones_v2.post("/concluir", response_model=CitClienteRecuperacionConcluirOut)
async def recuperar_contrasena_concluir(
    recuperacion: CitClienteRecuperacionConcluirIn,
    db: Session = Depends(get_db),
):
    """Olvide mi contrasena, recibo el formulario para cambiarla"""
    try:
        cit_cliente_recuperacion = terminate_recover_password(db, recuperacion)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRecuperacionConcluirOut.from_orm(cit_cliente_recuperacion)
