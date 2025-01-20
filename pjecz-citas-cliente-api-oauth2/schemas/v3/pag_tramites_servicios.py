"""
Pagos Trámites y Servicios V3, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class PagTramiteServicioOut(BaseModel):
    """Esquema para entregar tramites y servicios"""

    id_hasheado: str | None
    clave: str | None
    descripcion: str | None
    costo: float | None
    url: str | None
    model_config = ConfigDict(from_attributes=True)


class OnePagTramiteServicioOut(PagTramiteServicioOut, OneBaseOut):
    """Esquema para entregar un tramite y servicio"""
