"""
Cit Servicios V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class CitServicioOut(BaseModel):
    """Esquema para entregar servicio"""

    id: int | None = None
    cit_categoria_id: int | None = None
    cit_categoria_nombre: str | None = None
    clave: str | None = None
    descripcion: str | None = None
    documentos_limite: int | None = None
    model_config = ConfigDict(from_attributes=True)
