"""
Distritos V3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class DistritoOut(BaseModel):
    """Esquema para entregar distritos"""

    id_hasheado: str | None
    nombre: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneDistritoOut(DistritoOut, OneBaseOut):
    """Esquema para entregar un distrito"""
