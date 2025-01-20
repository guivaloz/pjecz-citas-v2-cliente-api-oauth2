"""
Autoridades V2, esquemas
"""

from pydantic import BaseModel, ConfigDict


class AutoridadOut(BaseModel):
    """Esquema para entregar autoridad"""

    id: int | None = None
    clave: str | None = None
    distrito_id: int | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    materia_id: int | None = None
    materia_nombre: str | None = None
    descripcion: str | None = None
    descripcion_corta: str | None = None
    organo_jurisdiccional: str | None = None
    model_config = ConfigDict(from_attributes=True)
