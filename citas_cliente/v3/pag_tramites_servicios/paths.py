"""
Pagos Tramites y Servicios V3, rutas (paths)
"""
from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_pag_tramites_servicios, get_pag_tramite_servicio
from .schemas import PagTramiteServicioOut, OnePagTramiteServicioOut

pag_tramites_servicios = APIRouter(prefix="/v3/pag_tramites_servicios", tags=["pagos"])


@pag_tramites_servicios.get("", response_model=CustomPage[PagTramiteServicioOut])
async def listado_pag_tramites_servicios(
    db: Session = Depends(get_db),
):
    """Listado de tramites y servicios"""
    try:
        resultados = get_pag_tramites_servicios(db=db)
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@pag_tramites_servicios.get("/{clave}", response_model=OnePagTramiteServicioOut)
async def detalle_pag_tramite_servicio(
    clave: str,
    db: Session = Depends(get_db),
):
    """Detalle de un tramite y servicio a partir de su id"""
    try:
        pag_tramite_servicio = get_pag_tramite_servicio(
            db=db,
            clave=clave,
        )
    except CitasAnyError as error:
        return OnePagTramiteServicioOut(success=False, message=str(error))
    return OnePagTramiteServicioOut.from_orm(pag_tramite_servicio)
