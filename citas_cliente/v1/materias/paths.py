"""
Materias v1.0, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..autoridades.crud import get_autoridades
from ..autoridades.schemas import AutoridadOut
from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_materias, get_materia
from .schemas import MateriaOut

materias = APIRouter(prefix="/v1/materias", tags=["materias"])


@materias.get("", response_model=LimitOffsetPage[MateriaOut])
async def listado_materias(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de materias"""
    if "MATERIAS" not in current_user.permissions or current_user.permissions["MATERIAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    return paginate(get_materias(db))


@materias.get("/{materia_id}", response_model=MateriaOut)
async def detalle_materia(
    materia_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una materia a partir de su id"""
    if "MATERIAS" not in current_user.permissions or current_user.permissions["MATERIAS"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        materia = get_materia(db, materia_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    return MateriaOut.from_orm(materia)


@materias.get("/{materia_id}/autoridades", response_model=LimitOffsetPage[AutoridadOut])
async def listado_autoridades_de_materia(
    materia_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de autoridades de una materia"""
    if "AUTORIDADES" not in current_user.permissions or current_user.permissions["AUTORIDADES"] < Permiso.VER:
        raise HTTPException(status_code=403, detail="Forbidden")
    try:
        listado = get_autoridades(db, materia_id=materia_id)
    except IndexError as error:
        raise HTTPException(status_code=404, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=406, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)
