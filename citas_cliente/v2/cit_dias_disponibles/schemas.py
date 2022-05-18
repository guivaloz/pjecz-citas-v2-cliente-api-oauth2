"""
Cit Dias Disponibles V2, esquemas de pydantic
"""
from datetime import date
from pydantic import BaseModel


class CitDiaDisponibleOut(BaseModel):
    """Esquema para entregar dias disponibles"""

    fecha: date
