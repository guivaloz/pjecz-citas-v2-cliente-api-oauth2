"""
Autoridades v1, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_autoridades, get_autoridad, get_autoridad_from_clave
from .schemas import AutoridadOut

autoridades = APIRouter(prefix="/v1/autoridades", tags=["autoridades"])


@autoridades.get("", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades(
    distrito_id: int = None,
    materia_id: int = None,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_autoridades(
            db,
            distrito_id=distrito_id,
            materia_id=materia_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@autoridades.get("/clave/{autoridad_clave}", response_model=AutoridadOut)
async def detalle_autoridad_con_clave(
    autoridad_clave: str,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su clave"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad_from_clave(db, clave=autoridad_clave)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)


@autoridades.get("/{autoridad_id}", response_model=AutoridadOut)
async def detalle_autoridad(
    autoridad_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una autoridad a partir de su id"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        autoridad = get_autoridad(db, autoridad_id=autoridad_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return AutoridadOut.from_orm(autoridad)
