"""
Cit Clientes Registros v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from lib.database import get_db

from .crud import post_cit_cliente_registro
from .schemas import CitClienteRegistroIn, CitClienteRegistroOut

cit_clientes_registros = APIRouter(prefix="/v1/cit_clientes_registros", tags=["clientes"])


@cit_clientes_registros.post("", response_model=CitClienteRegistroOut)
async def registrar_nueva_cuenta_de_cliente(
    registro: CitClienteRegistroIn,
    db: Session = Depends(get_db),
):
    """Registrar nueva cuenta de cliente"""
    try:
        cit_cliente_registro = post_cit_cliente_registro(db, registro)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitClienteRegistroOut.from_orm(cit_cliente_registro)
