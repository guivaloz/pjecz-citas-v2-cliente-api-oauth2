"""
Distritos V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.autoridades import get_autoridades
from ...cruds.v2.distritos import get_distrito, get_distritos
from ...dependencies.database import get_db
from ...dependencies.fastapi_pagination import LimitOffsetPage
from ...models.permisos import Permiso
from ...schemas.v2.autoridades import AutoridadOut
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.distritos import DistritoOut

distritos = APIRouter(prefix="/v2/distritos", tags=["distritos"])


@distritos.get("", response_model=LimitOffsetPage[DistritoOut])
async def listado_distritos(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de distritos"""
    if "DISTRITOS" not in current_user.permissions or current_user.permissions["DISTRITOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_distritos(db))


@distritos.get("/{distrito_id}", response_model=DistritoOut)
async def detalle_distrito(
    distrito_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de un distrito"""
    if "DISTRITOS" not in current_user.permissions or current_user.permissions["DISTRITOS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        distrito = get_distrito(db, distrito_id=distrito_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    return DistritoOut.from_orm(distrito)


@distritos.get("/{distrito_id}/autoridades", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades_del_distrito(
    distrito_id: int,
    materia_id: int = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades del distrito"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            materia_id=materia_id,
            son_notarias=False,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
