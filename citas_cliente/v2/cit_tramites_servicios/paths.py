"""
CIT TRAMITES SERVICIOS V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_cit_tramites_servicios, get_cit_tramite_servicio
from .schemas import CitTramiteServicioOut

cit_tramites_servicios = APIRouter(prefix="/v2/cit_tramites_servicios", tags=["tramites y servicios"])


@cit_tramites_servicios.get("", response_model=LimitOffsetPage[CitTramiteServicioOut])
async def listado_cit_tramites_servicios(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de tramites y servicios"""
    if "CIT TRAMITES SERVICIOS" not in current_user.permissions or current_user.permissions["CIT TRAMITES SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_tramites_servicios(db)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_tramites_servicios.get("/{cit_tramite_servicio_id}", response_model=CitTramiteServicioOut)
async def detalle_cit_tramite_servicio(
    cit_tramite_servicio_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un tramite y servicio a partir de su id"""
    if "CIT TRAMITES SERVICIOS" not in current_user.permissions or current_user.permissions["CIT TRAMITES SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_tramite_servicio = get_cit_tramite_servicio(db, cit_tramite_servicio_id=cit_tramite_servicio_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitTramiteServicioOut.from_orm(cit_tramite_servicio)
