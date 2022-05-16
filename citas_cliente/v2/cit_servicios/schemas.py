"""
Cit Servicios V2, esquemas de pydantic
"""
from pydantic import BaseModel


class CitServicioOut(BaseModel):
    """Esquema para entregar servicio"""

    id: int
    cit_categoria_id: int
    cit_categoria_nombre: str
    clave: str
    descripcion: str
    documentos_limite: int

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
