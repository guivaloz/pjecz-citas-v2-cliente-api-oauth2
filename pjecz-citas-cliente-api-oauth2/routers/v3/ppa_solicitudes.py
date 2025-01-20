"""
Pago de Pensiones Alimenticias - Solicitudes V3, rutas (paths)
"""

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ...cruds.v3.ppa_solicitudes import (
    create_ppa_solicitud,
    get_ppa_solicitud_from_id_hasheado,
    upload_autorizacion,
    upload_comprobante_domicilio,
    upload_identificacion_oficial,
)
from ...dependencies.database import get_db
from ...dependencies.exceptions import CitasAnyError
from ...schemas.v3.ppa_solicitudes import OnePpaSolicitudOut, PpaSolicitudIn

ppa_solicitudes = APIRouter(prefix="/v3/ppa_solicitudes", tags=["pago de pensiones alimenticias"])


@ppa_solicitudes.post("/solicitar", response_model=OnePpaSolicitudOut)
async def solicitar(
    datos: PpaSolicitudIn,
    db: Session = Depends(get_db),
):
    """Recibir, crear y entregar la solicitud de pago de pensiones alimenticias"""
    try:
        ppa_solicitud_out = create_ppa_solicitud(db=db, datos=datos)
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@ppa_solicitudes.post("/subir/identificacion_oficial", response_model=OnePpaSolicitudOut)
async def subir_identificacion_oficial(
    id_hasheado: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Subir archivo de identificación oficial"""
    try:
        ppa_solicitud_out = upload_identificacion_oficial(
            db=db,
            id_hasheado=id_hasheado,
            identificacion_oficial=archivo.file.read(),
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@ppa_solicitudes.post("/subir/comprobante_domicilio", response_model=OnePpaSolicitudOut)
async def subir_comprobante_domicilio(
    id_hasheado: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Subir archivo de comprobante de domicilio"""
    try:
        ppa_solicitud_out = upload_comprobante_domicilio(
            db=db,
            id_hasheado=id_hasheado,
            comprobante_domicilio=archivo.file.read(),
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@ppa_solicitudes.post("/subir/autorizacion", response_model=OnePpaSolicitudOut)
async def subir_autorizacion(
    id_hasheado: str,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Subir archivo de autorización"""
    try:
        ppa_solicitud_out = upload_autorizacion(
            db=db,
            id_hasheado=id_hasheado,
            autorizacion=archivo.file.read(),
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@ppa_solicitudes.get("/{ppa_solicitud_id_hasheado}", response_model=OnePpaSolicitudOut)
async def detalle_ppa_solicitud(
    ppa_solicitud_id_hasheado: str,
    db: Session = Depends(get_db),
):
    """Detalle de una solicitud a partir de su id hasheado"""
    try:
        ppa_solicitud = get_ppa_solicitud_from_id_hasheado(
            db=db,
            ppa_solicitud_id_hasheado=ppa_solicitud_id_hasheado,
        )
    except CitasAnyError as error:
        return OnePpaSolicitudOut(success=False, message=str(error))
    return OnePpaSolicitudOut.from_orm(ppa_solicitud)
