"""
Ci Citas V2, rutas (paths)
"""
from datetime import date, time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.fastapi_pagination import LimitOffsetPage

from ..cit_clientes.authentications import get_current_active_user
from ..cit_clientes.schemas import CitClienteInDB
from ..permisos.models import Permiso
from .crud import cancel_cit_cita, create_cit_cita, get_cit_cita, get_cit_citas
from .schemas import CitCitaIn, CitCitaOut

cit_citas = APIRouter(prefix="/v2/cit_citas", tags=["citas"])


@cit_citas.get("", response_model=LimitOffsetPage[CitCitaOut])
async def listado_cit_citas(
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Listado de citas"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        listado = get_cit_citas(db, cit_cliente_id=current_user.id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return paginate(listado)


@cit_citas.get("/{cit_cita_id}", response_model=CitCitaOut)
async def detalle_cit_cita(
    cit_cita_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Detalle de una cita a partir de su id"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.VER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = get_cit_cita(db, cit_cliente_id=current_user.id, cit_cita_id=cit_cita_id)
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitCitaOut.from_orm(cit_cita)


@cit_citas.post("/nueva", response_model=CitCitaOut)
async def crear_cit_cita(
    datos: CitCitaIn,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Crear una cita"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.CREAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = create_cit_cita(
            db,
            cit_cliente_id=current_user.id,
            oficina_id=datos.oficina_id,
            cit_servicio_id=datos.cit_servicio_id,
            fecha=datos.fecha,
            hora_minuto=datos.hora_minuto,
            nota=datos.notas,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitCitaOut.from_orm(cit_cita)


@cit_citas.get("/cancelar/{cit_cita_id}", response_model=CitCitaOut)
async def cancelar_cit_citas(
    cit_cita_id: int,
    current_user: CitClienteInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Cancelar una cita"""
    if "CIT CITAS" not in current_user.permissions or current_user.permissions["CIT CITAS"] < Permiso.MODIFICAR:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    try:
        cit_cita = cancel_cit_cita(
            db,
            cit_cliente_id=current_user.id,
            cit_cita_id=cit_cita_id,
        )
    except IndexError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found: {str(error)}") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"Not acceptable: {str(error)}") from error
    return CitCitaOut.from_orm(cit_cita)
