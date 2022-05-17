"""
Cit Servicios V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_cit_servicios, get_cit_servicio
from .schemas import CitServicioOut

cit_servicios = APIRouter(prefix="/v2/cit_servicios", tags=["servicios"])


@cit_servicios.get("", response_model=LimitOffsetPage[CitServicioOut])
async def listado_cit_servicios(
    cit_categoria_id: int = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de servicios"""
    if "CIT SERVICIOS" not in current_user.permissions or current_user.permissions["CIT SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_cit_servicios(db, cit_categoria_id))


@cit_servicios.get("/{cit_servicio_id}", response_model=CitServicioOut)
async def detalle_cit_servicio(
    cit_servicio_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un servicio a partir de su id"""
    if "CIT SERVICIOS" not in current_user.permissions or current_user.permissions["CIT SERVICIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_servicio = get_cit_servicio(db, cit_servicio_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitServicioOut.from_orm(cit_servicio)
