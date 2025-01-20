"""
Domicilios V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.domicilios import get_domicilio, get_domicilios
from ...dependencies.database import get_db
from ...dependencies.fastapi_pagination import LimitOffsetPage
from ...models.permisos import Permiso
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.domicilios import DomicilioOut

domicilios_v2 = APIRouter(prefix="/v2/domicilios", tags=["oficinas"])


@domicilios_v2.get("", response_model=LimitOffsetPage[DomicilioOut])
async def listado_domicilios(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de domicilios"""
    if "DOMICILIOS" not in current_user.permissions or current_user.permissions["DOMICILIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_domicilios(db))


@domicilios_v2.get("/{domicilio_id}", response_model=DomicilioOut)
async def detalle_domicilio(
    domicilio_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un domicilio a partir de su id"""
    if "DOMICILIOS" not in current_user.permissions or current_user.permissions["DOMICILIOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        domicilio = get_domicilio(db, domicilio_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return DomicilioOut.from_orm(domicilio)
