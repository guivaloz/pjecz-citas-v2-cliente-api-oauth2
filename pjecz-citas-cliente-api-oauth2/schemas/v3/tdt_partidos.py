"""
Tres de Tres - Partidos V3, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class TdtPartidoOut(BaseModel):
    """Esquema para entregar partidos"""

    id_hasheado: str | None
    nombre: str | None
    siglas: str | None
    model_config = ConfigDict(from_attributes=True)


class OneTdtPartidoOut(TdtPartidoOut, OneBaseOut):
    """Esquema para entregar un partido"""
