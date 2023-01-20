"""
Pagos Pagos V3, rutas (paths)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError

from .crud import get_pag_pago, create_payment, update_payment
from .schemas import OnePagPagoOut, PagCarroIn, OnePagCarroOut, PagResultadoIn, OnePagResultadoOut

pag_pagos = APIRouter(prefix="/v2/pag_pagos", tags=["pagos"])


@pag_pagos.post("/carro", response_model=OnePagCarroOut)
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
    except CitasAnyError as error:
        return OnePagCarroOut(success=False, message=str(error))
    return pag_carro_out


@pag_pagos.post("/resultado", response_model=OnePagResultadoOut)
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
    except CitasAnyError as error:
        return OnePagResultadoOut(success=False, message=str(error))
    return pag_resultado_out


@pag_pagos.get("/{pag_pago_id_hasheado}", response_model=OnePagPagoOut)
async def detalle_pag_pago(
    pag_pago_id_hasheado: str,
    db: Session = Depends(get_db),
):
    """Detalle de un pago a partir de su id haseado"""
    try:
        pag_pago = get_pag_pago(
            db=db,
            pag_pago_id_hasheado=pag_pago_id_hasheado,
        )
    except CitasAnyError as error:
        return OnePagPagoOut(success=False, message=str(error))
    return pag_pago
