"""
Pago de Pensiones Alimenticias - Solicitudes V3, rutas (paths)
"""
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError

from .crud import get_ppa_solicitud_from_id_hasheado, create_ppa_solicitud
from .schemas import OnePpaSolicitudOut, PpaSolicitudIn

ppa_solicitudes = APIRouter(prefix="/v3/ppa_solicitudes", tags=["pago de pensiones alimenticias"])


@ppa_solicitudes.post("/solicitar", response_model=OnePpaSolicitudOut)
async def solicitar(
    datos: PpaSolicitudIn,
    identificacion_oficial: UploadFile = File(...),
    comprobante_domicilio: UploadFile = File(...),
    autorizacion: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Recibir, crear y entregar la solicitud de pago de pensiones alimenticias"""
    try:
        ppa_solicitud_out = create_ppa_solicitud(
            db=db,
            datos=datos,
            identificacion_oficial=identificacion_oficial.file.read(),
            comprobante_domicilio=comprobante_domicilio.file.read(),
            autorizacion=autorizacion.file.read(),
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@ppa_solicitudes.get("/{ppa_solicitud_id_hasheado}", response_model=OnePpaSolicitudOut)
async def detalle_ppa_solicitud(ppa_solicitud_id_hasheado: str, db: Session = Depends(get_db)):
    """Detalle de una solicitud a partir de su id hasheado"""
    try:
        ppa_solicitud = get_ppa_solicitud_from_id_hasheado(
            db=db,
            ppa_solicitud_id_hasheado=ppa_solicitud_id_hasheado,
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return OnePpaSolicitudOut.from_orm(ppa_solicitud)
