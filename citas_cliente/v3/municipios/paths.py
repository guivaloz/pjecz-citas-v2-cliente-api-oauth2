"""
Municipios V3, rutas (paths)
"""
from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from lib.database import get_db
from lib.exceptions import CitasAnyError
from lib.fastapi_pagination_custom_page import CustomPage, custom_page_success_false

from .crud import get_municipios, get_municipio_from_id_hasheado
from .schemas import MunicipioOut, OneMunicipioOut

municipios = APIRouter(prefix="/v3/municipios", tags=["municipios"])


@municipios.get("", response_model=CustomPage[MunicipioOut])
async def listado_municipios(db: Session = Depends(get_db)):
    """Listado de municipios"""
    try:
        resultados = get_municipios(db=db)
    except CitasAnyError as error:
        return custom_page_success_false(error)
    return paginate(resultados)


@municipios.get("/{municipio_id_hasheado}", response_model=OneMunicipioOut)
async def detalle_municipio(municipio_id_hasheado: str, db: Session = Depends(get_db)):
    """Detalle de un municipio a partir de su id"""
    try:
        municipio = get_municipio_from_id_hasheado(db=db, municipio_id_hasheado=municipio_id_hasheado)
    except CitasAnyError as error:
        return OneMunicipioOut(success=False, message=str(error))
    return OneMunicipioOut.from_orm(municipio)
