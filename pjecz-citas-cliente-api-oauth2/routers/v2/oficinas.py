"""
Oficinas V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.oficinas import get_oficina, get_oficinas
from ...dependencies.database import get_db
from ...dependencies.fastapi_pagination import LimitOffsetPage
from ...models.permisos import Permiso
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.oficinas import OficinaOut

oficinas_v2 = APIRouter(prefix="/v2/oficinas", tags=["oficinas"])


@oficinas_v2.get("/", response_model=LimitOffsetPage[OficinaOut])
async def listado_oficinas(
    distrito_id: int = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de oficinas"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_oficinas(
            db=db,
            distrito_id=distrito_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@oficinas_v2.get("/{oficina_id}", response_model=OficinaOut)
async def detalle_oficina(
    oficina_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una oficina a partir de su id"""
    if "OFICINAS" not in current_user.permissions or current_user.permissions["OFICINAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        oficina = get_oficina(db, oficina_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return OficinaOut.from_orm(oficina)
