"""
Tres de Tres - Partidos V3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class TdtPartidoOut(BaseModel):
    """Esquema para entregar partidos"""

    id: int | None
    nombre: str | None
    siglas: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneTdtPartidoOut(TdtPartidoOut, OneBaseOut):
    """Esquema para entregar un partido"""
