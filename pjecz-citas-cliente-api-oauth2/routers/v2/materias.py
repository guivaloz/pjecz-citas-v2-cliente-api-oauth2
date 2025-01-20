"""
Materias V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.autoridades import get_autoridades
from ...cruds.v2.materias import get_materia, get_materias
from ...dependencies.database import get_db
from ...dependencies.fastapi_pagination import LimitOffsetPage
from ...models.permisos import Permiso
from ...schemas.v2.autoridades import AutoridadOut
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.materias import MateriaOut

materias_v2 = APIRouter(prefix="/v2/materias", tags=["materias"])


@materias_v2.get("", response_model=LimitOffsetPage[MateriaOut])
async def listado_materias(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de materias"""
    if "MATERIAS" not in current_user.permissions or current_user.permissions["MATERIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_materias(db))


@materias_v2.get("/{materia_id}", response_model=MateriaOut)
async def detalle_materia(
    materia_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia a partir de su id"""
    if "MATERIAS" not in current_user.permissions or current_user.permissions["MATERIAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        materia = get_materia(db, materia_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    return MateriaOut.from_orm(materia)


@materias_v2.get("/{materia_id}/autoridades", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades_de_materia(
    materia_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades de una materia"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_autoridades(db, materia_id=materia_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
