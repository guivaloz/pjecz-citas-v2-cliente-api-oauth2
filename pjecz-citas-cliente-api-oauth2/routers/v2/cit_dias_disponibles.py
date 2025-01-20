"""
Cit Dias Disponibles V2, rutas (paths)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from ...cruds.v2.authentications import get_current_active_user
from ...cruds.v2.cit_dias_disponibles import get_cit_dias_disponibles
from ...dependencies.database import get_db
from ...models.permisos import Permiso
from ...schemas.v2.cit_clientes import CitClienteInDB
from ...schemas.v2.cit_dias_disponibles import CitDiaDisponibleOut

cit_dias_disponibles_v2 = APIRouter(prefix="/v2/cit_dias_disponibles", tags=["dias disponibles"])


@cit_dias_disponibles_v2.get("", response_model=Page[CitDiaDisponibleOut])
async def listado_cit_dias_disponibles(
    oficina_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de dias disponibles"""
    if "CIT DIAS DISPONIBLES" not in current_user.permissions or current_user.permissions["CIT DIAS DISPONIBLES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    resultado = [CitDiaDisponibleOut(fecha=item) for item in get_cit_dias_disponibles(db, oficina_id)]
    return paginate(resultado)
