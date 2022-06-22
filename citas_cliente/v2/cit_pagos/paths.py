"""
Cit Pagos V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_cit_pagos, get_cit_pago, create_cit_pago, process_cit_pago
from .schemas import CitPagoNuevoIn, CitPagoRealizadoIn, CitPagoOut

cit_pagos = APIRouter(prefix="/v2/cit_pagos", tags=["pagos"])


@cit_pagos.post("/nuevo", response_model=CitPagoOut)
async def crear_cit_pago(
    datos: CitPagoNuevoIn,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Crear un pago"""
    if "CIT PAGOS" not in current_user.permissions or current_user.permissions["CIT PAGOS"] < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_pago = create_cit_pago(
            db,
            nombres=datos.nombres,
            apellido_primero=datos.apellido_primero,
            apellido_segundo=datos.apellido_segundo,
            curp=datos.curp,
            telefono=datos.telefono,
            email=datos.email,
            cit_tramite_servicio_id=datos.cit_tramite_servicio_id,
            cantidad=datos.cantidad,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitPagoOut.from_orm(cit_pago)


@cit_pagos.post("/realizado", response_model=CitPagoOut)
async def realizar_cit_pago(
    datos: CitPagoRealizadoIn,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Realizar un pago, es decir, atrapar los datos que manda el banco de este pago"""
    if "CIT PAGOS" not in current_user.permissions or current_user.permissions["CIT PAGOS"] < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_pago = process_cit_pago(
            db,
            id=datos.id,
            folio=datos.folio,
            estado=datos.estado,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitPagoOut.from_orm(cit_pago)


@cit_pagos.get("", response_model=LimitOffsetPage[CitPagoOut])
async def listado_cit_pagos(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de pagos"""
    if "CIT PAGOS" not in current_user.permissions or current_user.permissions["CIT PAGOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_pagos(db, cit_cliente_id=current_user.id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_pagos.get("/{cit_pago_id}", response_model=CitPagoOut)
async def detalle_cit_pago(
    cit_pago_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un pago a partir de su id"""
    if "CIT PAGOS" not in current_user.permissions or current_user.permissions["CIT PAGOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_pago = get_cit_pago(db, cit_pago_id=cit_pago_id)
        if cit_pago.cit_cliente_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitPagoOut.from_orm(cit_pago)
