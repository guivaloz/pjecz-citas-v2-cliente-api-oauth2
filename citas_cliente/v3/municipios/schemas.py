"""
Municipios V3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class MunicipioOut(BaseModel):
    """Esquema para entregar comentario"""

    id_hasheado: str | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneMunicipioOut(MunicipioOut, OneBaseOut):
    """Esquema para entregar un comentario"""
