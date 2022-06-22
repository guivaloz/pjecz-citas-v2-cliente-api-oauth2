"""
Cit Tramites Servicios V2, esquemas de pydantic
"""
from pydantic import BaseModel


class CitTramiteServicioOut(BaseModel):
    """Esquema para entregar tramites y servicios"""

    id: int
    nombre: str
    costo: float
    url: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
