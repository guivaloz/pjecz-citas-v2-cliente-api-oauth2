"""
Cit Oficinas Servicios V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.cit_oficinas_servicios import get_cit_oficina_servicio, get_cit_oficinas_servicios
from ...dependencies.database import get_db
from ...dependencies.fastapi_pagination import LimitOffsetPage
from ...models.permisos import Permiso
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.cit_oficinas_servicios import CitOficinaServicioOut

cit_oficinas_servicios_v2 = APIRouter(prefix="/v2/cit_oficinas_servicios", tags=["servicios"])


@cit_oficinas_servicios_v2.get("", response_model=LimitOffsetPage[CitOficinaServicioOut])
async def listado_cit_oficinas_servicios(
    cit_servicio_id: int = None,
    oficina_id: int = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas-servicios"""
    if (
        "CIT OFICINAS SERVICIOS" not in current_user.permissions
        or current_user.permissions["CIT OFICINAS SERVICIOS"] < Permiso.VER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_cit_oficinas_servicios(db, cit_servicio_id, oficina_id))


@cit_oficinas_servicios_v2.get("/{cit_oficina_servicio_id}", response_model=CitOficinaServicioOut)
async def detalle_cit_oficina_servicio(
    cit_oficina_servicio_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un oficina-servicio a partir de su id"""
    if (
        "CIT OFICINAS SERVICIOS" not in current_user.permissions
        or current_user.permissions["CIT OFICINAS SERVICIOS"] < Permiso.VER
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_oficina_servicio = get_cit_oficina_servicio(db, cit_oficina_servicio_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitOficinaServicioOut.from_orm(cit_oficina_servicio)
