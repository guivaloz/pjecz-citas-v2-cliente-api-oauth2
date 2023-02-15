"""
Cit Clientes Registros V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import request_new_account, validate_new_account, terminate_new_account
from .schemas import CitClienteRegistroIn, CitClienteRegistroOut, CitClienteRegistroValidarOut, CitClienteRegistroConcluirIn, CitClienteRegistroConcluirOut

cit_clientes_registros_v2 = APIRouter(prefix="/v2/nueva_cuenta", tags=["nueva cuenta"])


@cit_clientes_registros_v2.post("/solicitar", response_model=CitClienteRegistroOut)
async def nueva_cuenta_solicitar(
    registro: CitClienteRegistroIn,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, recibo el formulario con los datos personales"""
    try:
        cit_cliente_registro = request_new_account(db, registro)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroOut.from_orm(cit_cliente_registro)


@cit_clientes_registros_v2.get("/validar", response_model=CitClienteRegistroValidarOut)
async def nueva_cuenta_validar(
    hashid: str = None,
    cadena_validar: str = None,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, viene del URL proporcionado, entrego el formulario para definir la contrasena"""
    if not isinstance(hashid, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    if not isinstance(cadena_validar, str):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    try:
        cit_cliente_registro = validate_new_account(db, hashid, cadena_validar)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroValidarOut.from_orm(cit_cliente_registro)


@cit_clientes_registros_v2.post("/concluir", response_model=CitClienteRegistroConcluirOut)
async def nueva_cuenta_concluir(
    registro: CitClienteRegistroConcluirIn,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, recibo el formulario con la contrasena"""
    try:
        cit_cliente_registro = terminate_new_account(db, registro)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroConcluirOut.from_orm(cit_cliente_registro)
