"""
Tres de Tres - Partidos V3, rutas (paths)
"""

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v3.tdt_partidos import get_tdt_partido_from_siglas, get_tdt_partidos
from ...dependencies.database import get_db
from ...dependencies.exceptions import CitasAnyError
from ...dependencies.fastapi_pagination_custom_page import CustomPage, custom_page_success_false
from ...schemas.v3.tdt_partidos import OneTdtPartidoOut, TdtPartidoOut

tdt_partidos = APIRouter(prefix="/v3/tdt_partidos", tags=["tres de tres"])


@tdt_partidos.get("", response_model=CustomPage[TdtPartidoOut])
async def listado_tdt_partidos(db: Session = Depends(get_db)):
    """Listado de partidos"""
    try:
        resultados = get_tdt_partidos(db=db)
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@tdt_partidos.get("/{tdt_partido_siglas}", response_model=OneTdtPartidoOut)
async def detalle_tdt_partido(tdt_partido_siglas: str, db: Session = Depends(get_db)):
    """Detalle de un partido a partir de sus siglas"""
    try:
        tdt_partido = get_tdt_partido_from_siglas(db=db, siglas=tdt_partido_siglas)
    except CitasAnyError as error:
        return OneTdtPartidoOut(success=False, message=str(error))
    return OneTdtPartidoOut.from_orm(tdt_partido)
