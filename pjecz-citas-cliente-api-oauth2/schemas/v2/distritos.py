"""
Distritos V2, esquemas
"""

from pydantic import BaseModel, ConfigDict


class DistritoOut(BaseModel):
    """Esquema para entregar distrito"""

    id: int | None = None
    clave: str | None = None
    nombre: str | None = None
    nombre_corto: str | None = None
    model_config = ConfigDict(from_attributes=True)
