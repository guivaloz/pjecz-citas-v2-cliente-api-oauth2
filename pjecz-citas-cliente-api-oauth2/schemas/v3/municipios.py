"""
Municipios V3, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class MunicipioOut(BaseModel):
    """Esquema para entregar comentario"""

    id_hasheado: str | None
    nombre: str | None
    model_config = ConfigDict(from_attributes=True)


class OneMunicipioOut(MunicipioOut, OneBaseOut):
    """Esquema para entregar un comentario"""
