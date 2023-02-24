"""
Tres de Tres - Solicitudes V3, rutas (paths)
"""
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError

from .crud import (
    get_tdt_solicitud_from_id_hasheado,
    create_tdt_solicitud,
    upload_identificacion_oficial,
    upload_comprobante_domicilio,
    upload_autorizacion,
)
from .schemas import OneTdtSolicitudOut, TdtSolicitudIn

tdt_solicitudes = APIRouter(prefix="/v3/tdt_solicitudes", tags=["tres de tres"])


@tdt_solicitudes.post("/solicitar", response_model=OneTdtSolicitudOut)
async def solicitar(datos: TdtSolicitudIn, db: Session = Depends(get_db)):
    """Recibir, crear y entregar la solicitud de tres de tres"""
    try:
        tdt_solicitud_out = create_tdt_solicitud(
            db=db,
            datos=datos,
        )
    except CitasAnyError as error:
        return OneTdtSolicitudOut(success=False, message=str(error))
    return tdt_solicitud_out


@tdt_solicitudes.post("/subir/identificacion_oficial", response_model=OneTdtSolicitudOut)
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
        return OneTdtSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@tdt_solicitudes.post("/subir/comprobante_domicilio", response_model=OneTdtSolicitudOut)
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
        return OneTdtSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@tdt_solicitudes.post("/subir/autorizacion", response_model=OneTdtSolicitudOut)
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
        return OneTdtSolicitudOut(success=False, message=str(error))
    return ppa_solicitud_out


@tdt_solicitudes.get("/{tdt_solicitud_id_hasheado}", response_model=OneTdtSolicitudOut)
async def detalle_tdt_solicitud(tdt_solicitud_id_hasheado: str, db: Session = Depends(get_db)):
    """Detalle de una solicitud a partir de su id hasheado"""
    try:
        tdt_solicitud = get_tdt_solicitud_from_id_hasheado(
            db=db,
            tdt_solicitud_id_hasheado=tdt_solicitud_id_hasheado,
        )
    except CitasAnyError as error:
        return OneTdtSolicitudOut(success=False, message=str(error))
    return OneTdtSolicitudOut.from_orm(tdt_solicitud)
