"""
Distritos V3, rutas (paths)
"""
from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_distritos, get_distrito_from_id_hasheado
from .schemas import DistritoOut, OneDistritoOut

distritos = APIRouter(prefix="/v3/distritos", tags=["distritos"])


@distritos.get("", response_model=CustomPage[DistritoOut])
async def listado_distritos(db: Session = Depends(get_db)):
    """Listado de distritos"""
    try:
        resultados = get_distritos(db=db)
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@distritos.get("/{distrito_id_hasheado}", response_model=OneDistritoOut)
async def detalle_distrito(distrito_id_hasheado: str, db: Session = Depends(get_db)):
    """Detalle de un distrito a partir de su id"""
    try:
        distrito = get_distrito_from_id_hasheado(db=db, distrito_id_hasheado=distrito_id_hasheado)
    except CitasAnyError as error:
        return OneDistritoOut(success=False, message=str(error))
    return OneDistritoOut.from_orm(distrito)
