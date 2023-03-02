"""
Distritos V2, esquemas
"""
from pydantic import BaseModel


class DistritoOut(BaseModel):
    """Esquema para entregar distrito"""

    id: int
    clave: str
    nombre: str
    nombre_corto: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
