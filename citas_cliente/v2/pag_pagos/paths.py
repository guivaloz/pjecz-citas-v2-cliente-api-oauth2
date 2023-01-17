"""
Pagos Pagos V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_pag_pagos, get_pag_pago, create_payment, update_payment
from .schemas import PagPagoOut, PagCarroIn, PagCarroOut, PagResultadoIn, PagResultadoOut

pag_pagos = APIRouter(prefix="/v2/pag_pagos", tags=["pagos"])


@pag_pagos.get("", response_model=LimitOffsetPage[PagPagoOut])
async def listado_pag_pagos(
    estado: str = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de pagos"""
    if "PAG PAGOS" not in current_user.permissions or current_user.permissions["PAG PAGOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_pag_pagos(
            db=db,
            cit_cliente_id=current_user.cit_cliente_id,
            estado=estado,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@pag_pagos.post("/carro", response_model=PagCarroOut)
async def carro(
    datos: PagCarroIn,
    db: Session = Depends(get_db),
):
    """Recibir, procesar y entregar datos del carro de pagos"""
    try:
        pag_carro_out = create_payment(
            db=db,
            datos=datos,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return pag_carro_out


@pag_pagos.post("/resultado", response_model=PagResultadoOut)
async def resultado(
    datos: PagResultadoIn,
    db: Session = Depends(get_db),
):
    """Recibir, procesar y entregar datos del resultado de pagos"""
    try:
        pag_resultado_out = update_payment(
            db=db,
            datos=datos,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return pag_resultado_out


@pag_pagos.get("/{pag_pago_id_hasheado}", response_model=PagPagoOut)
async def detalle_pag_pago(
    pag_pago_id_hasheado: str,
    db: Session = Depends(get_db),
):
    """Detalle de un pago a partir de su id"""
    try:
        pag_pago = get_pag_pago(
            db=db,
            pag_pago_id_hasheado=pag_pago_id_hasheado,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return PagPagoOut.from_orm(pag_pago)
