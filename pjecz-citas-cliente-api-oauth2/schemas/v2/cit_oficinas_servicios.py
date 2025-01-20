"""
Cit Oficinas Servicios V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficina-servicio"""

    id: int | None = None
    cit_servicio_id: int | None = None
    cit_servicio_clave: str | None = None
    cit_servicio_descripcion: str | None = None
    oficina_id: int | None = None
    oficina_clave: str | None = None
    oficina_descripcion: str | None = None
    oficina_descripcion_corta: str | None = None
    model_config = ConfigDict(from_attributes=True)
