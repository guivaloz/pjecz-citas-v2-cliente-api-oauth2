"""
Ci Citas V2, rutas (paths)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_cit_citas
from .schemas import CitCitaOut

cit_citas = APIRouter(prefix="/v2/cit_citas", tags=["citas"])


@cit_citas.get("", response_model=LimitOffsetPage[CitCitaOut])
async def listado_cit_citas(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de citas"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return paginate(get_cit_citas(db, cit_cliente_id=current_user.id))
