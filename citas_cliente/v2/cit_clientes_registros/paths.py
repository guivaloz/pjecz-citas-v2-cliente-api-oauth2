"""
Cit Clientes Registros V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import post_cit_cliente_registro
from .schemas import CitClienteRegistroIn, CitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/v2/nueva_cuenta", tags=["nueva cuenta"])


@cit_clientes_registros.post("/solicitar", response_model=CitClienteRegistroOut)
async def solicitar_nueva_cuenta(
    registro: CitClienteRegistroIn,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, recibo el formulario con los datos personales"""
    try:
        cit_cliente_registro = post_cit_cliente_registro(db, registro)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroOut.from_orm(cit_cliente_registro)


@cit_clientes_registros.get("/validar/<hashid:str>/<cadena_validar:str>", response_model=CitClienteRegistroOut)
async def validar_nueva_cuenta(
    hashid: str,
    cadena_validar: str,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, viene del URL proporcionado, entrego el formulario para definir la contrasena"""


@cit_clientes_registros.post("/concluir", response_model=CitClienteRegistroOut)
async def concluir_nueva_cuenta(
    registro: CitClienteRegistroIn,
    db: Session = Depends(get_db),
):
    """Quiero crear una nueva cuenta, recibo el formulario con la contrasena"""
