"""
Cit Citas Horas Disponibles V2, rutas (paths)
"""
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from lib.database import get_db

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import get_cit_horas_disponibles
from .schemas import CitHoraDisponibleOut

cit_horas_disponibles = APIRouter(prefix="/v2/cit_horas_disponibles", tags=["horas disponibles"])


@cit_horas_disponibles.get("", response_model=Page[CitHoraDisponibleOut])
async def listado_cit_horas_disponibles(
    oficina_id: int,
    cit_servicio_id: int,
    fecha: date,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de horas disponibles"""
    if "CIT HORAS DISPONIBLES" not in current_user.permissions or current_user.permissions["CIT HORAS DISPONIBLES"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    resultado = [CitHoraDisponibleOut(horas_minutos=item) for item in get_cit_horas_disponibles(db, oficina_id=oficina_id, cit_servicio_id=cit_servicio_id, fecha=fecha)]
    return paginate(resultado)
