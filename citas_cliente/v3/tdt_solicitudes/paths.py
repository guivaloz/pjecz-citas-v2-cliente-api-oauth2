"""
Tres de Tres - Solicitudes V3, rutas (paths)
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError

from .crud import get_tdt_solicitud, create_tdt_solicitud
from .schemas import OneTdtSolicitudOut, TdtSolicitudIn

tdt_solicitudes = APIRouter(prefix="/v3/tdt_solicitudes", tags=["tres de tres"])


@tdt_solicitudes.post("/solicitar", response_model=OneTdtSolicitudOut)
async def solicitar(
    datos: TdtSolicitudIn,
    db: Session = Depends(get_db),
):
    """Recibir, crear y entregar la solicitud de tres de tres"""
    try:
        tdt_solicitud_out = create_tdt_solicitud(
            db=db,
            datos=datos,
        )
    except CitasAnyError as error:
        return OneTdtSolicitudOut(success=False, message=str(error))
    return tdt_solicitud_out


@tdt_solicitudes.get("/{tdt_solicitud_id_hasheado}", response_model=OneTdtSolicitudOut)
async def detalle_tdt_solicitud(
    tdt_solicitud_id_hasheado: int,
    db: Session = Depends(get_db),
):
    """Detalle de una solicitud a partir de su id hasheado"""
    try:
        tdt_solicitud = get_tdt_solicitud(
            db=db,
            tdt_solicitud_id_hasheado=tdt_solicitud_id_hasheado,
        )
    except CitasAnyError as error:
        return OneTdtSolicitudOut(success=False, message=str(error))
    return OneTdtSolicitudOut.from_orm(tdt_solicitud)
