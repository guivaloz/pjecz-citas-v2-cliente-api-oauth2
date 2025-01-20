"""
Oficinas V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class OficinaOut(BaseModel):
    """Esquema para entregar oficinas"""

    id: int | None = None
    distrito_id: int | None = None
    distrito_nombre: str | None = None
    distrito_nombre_corto: str | None = None
    domicilio_id: int | None = None
    domicilio_completo: str | None = None
    clave: str | None = None
    descripcion: str | None = None
    descripcion_corta: str | None = None
    model_config = ConfigDict(from_attributes=True)
