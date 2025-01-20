"""
Autoridades V3, rutas (paths)
"""

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from ...cruds.v3.autoridades import get_autoridad_from_clave, get_autoridades
from ...dependencies.database import get_db
from ...dependencies.exceptions import CitasAnyError
from ...dependencies.fastapi_pagination_custom_page import CustomPage, custom_page_success_false
from ...schemas.v3.autoridades import AutoridadOut, OneAutoridadOut

autoridades = APIRouter(prefix="/v3/autoridades", tags=["autoridades"])


@autoridades.get("", response_model=CustomPage[AutoridadOut])
async def listado_autoridades(db: Session = Depends(get_db)):
    """Listado de autoridades"""
    try:
        resultados = get_autoridades(db=db)
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@autoridades.get("/{clave}", response_model=OneAutoridadOut)
async def detalle_autoridad(clave: str, db: Session = Depends(get_db)):
    """Detalle de una autoridad a partir de su clave"""
    try:
        autoridad = get_autoridad_from_clave(db=db, clave=clave)
    except CitasAnyError as error:
        return OneAutoridadOut(success=False, message=str(error))
    return OneAutoridadOut.from_orm(autoridad)
