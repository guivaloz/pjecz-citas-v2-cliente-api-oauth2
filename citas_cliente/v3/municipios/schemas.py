"""
Municipios V3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class EsquemaOut(BaseModel):
    """Esquema para entregar comentario"""

    id: int | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneEsquemaOut(EsquemaOut, OneBaseOut):
    """Esquema para entregar un comentario"""
