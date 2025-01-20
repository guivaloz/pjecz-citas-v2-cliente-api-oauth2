"""
Distritos V3, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id_hasheado: str | None
    clave: str | None
    nombre: str | None
    nombre_corto: str | None
    model_config = ConfigDict(from_attributes=True)


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
