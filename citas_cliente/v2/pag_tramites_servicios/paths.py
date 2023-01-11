"""
Pag Tramites y Servicios V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_pag_tramites_servicios, get_pag_tramite_servicio
from .schemas import PagTramiteServicioOut

pag_tramites_servicios = APIRouter(prefix="/v2/pag_tramites_servicios", tags=["pagos"])


@pag_tramites_servicios.get("", response_model=LimitOffsetPage[PagTramiteServicioOut])
async def listado_pag_tramites_servicios(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tramites y servicios"""
    if "PAG TRAMITES SERVICIOS" not in current_user.permissions or current_user.permissions["PAG TRAMITES SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_pag_tramites_servicios(db))


@pag_tramites_servicios.get("/{pag_tramite_servicio_id}", response_model=PagTramiteServicioOut)
async def detalle_pag_tramite_servicio(
    pag_tramite_servicio_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un tramite y servicio a partir de su id"""
    if "PAG TRAMITES SERVICIOS" not in current_user.permissions or current_user.permissions["PAG TRAMITES SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        pag_tramite_servicio = get_pag_tramite_servicio(
            db=db,
            pag_tramite_servicio_id=pag_tramite_servicio_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return PagTramiteServicioOut.from_orm(pag_tramite_servicio)
