"""
Autoridades V3, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridades"""

    id_hasheado: str | None
    clave: str | None
    descripcion: str | None
    descripcion_corta: str | None
    distrito_nombre: str | None
    model_config = ConfigDict(from_attributes=True)


class OneAutoridadOut(AutoridadOut, OneBaseOut):
    """Esquema para entregar una autoridad"""
