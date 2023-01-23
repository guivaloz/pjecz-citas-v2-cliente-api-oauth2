"""
Pagos Tramites y Servicios V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from .crud import get_pag_tramites_servicios, get_pag_tramite_servicio_from_clave
from .schemas import PagTramiteServicioOut

pag_tramites_servicios = APIRouter(prefix="/v2/pag_tramites_servicios", tags=["pagos v2"])


@pag_tramites_servicios.get("", response_model=LimitOffsetPage[PagTramiteServicioOut])
async def listado_pag_tramites_servicios(
    db: Session = Depends(get_db),
):
    """Listado de tramites y servicios"""
    return paginate(get_pag_tramites_servicios(db))


@pag_tramites_servicios.get("/{clave}", response_model=PagTramiteServicioOut)
async def detalle_pag_tramite_servicio(
    clave: str,
    db: Session = Depends(get_db),
):
    """Detalle de un tramite y servicio a partir de su id"""
    try:
        pag_tramite_servicio = get_pag_tramite_servicio_from_clave(
            db=db,
            clave=clave,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return PagTramiteServicioOut.from_orm(pag_tramite_servicio)
