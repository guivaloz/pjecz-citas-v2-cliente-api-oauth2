"""
Pagos Pagos V3, rutas (paths)
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...cruds.v3.pag_pagos import create_payment, get_pag_pago_from_id_hasheado, update_payment
from ...dependencies.database import get_db
from ...dependencies.exceptions import CitasAnyError
from ...schemas.v3.pag_pagos import OnePagCarroOut, OnePagPagoOut, OnePagResultadoOut, PagCarroIn, PagResultadoIn

pag_pagos = APIRouter(prefix="/v3/pag_pagos", tags=["pagos"])


@pag_pagos.post("/carro", response_model=OnePagCarroOut)
async def carro(datos: PagCarroIn, db: Session = Depends(get_db)):
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
async def resultado(datos: PagResultadoIn, db: Session = Depends(get_db)):
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
async def detalle_pag_pago(pag_pago_id_hasheado: str, db: Session = Depends(get_db)):
    """Detalle de un pago a partir de su id hasheado"""
    try:
        pag_pago = get_pag_pago_from_id_hasheado(
            db=db,
            pag_pago_id_hasheado=pag_pago_id_hasheado,
        )
    except CitasAnyError as error:
        return OnePagPagoOut(success=False, message=str(error))
    return pag_pago
