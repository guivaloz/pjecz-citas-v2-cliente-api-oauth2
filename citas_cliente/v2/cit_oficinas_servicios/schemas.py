"""
Cit Oficinas Servicios V2, esquemas de pydantic
"""
from pydantic import BaseModel


class CitOficinaServicioOut(BaseModel):
    """Esquema para entregar oficina-servicio"""

    id: int
    cit_servicio_id: int
    cit_servicio_clave: str
    cit_servicio_descripcion: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
