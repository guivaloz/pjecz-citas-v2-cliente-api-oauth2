"""
Cit Citas V2, esquemas de pydantic
"""
from datetime import datetime, date, time
from typing import Optional
from pydantic import BaseModel


class CitCitaIn(BaseModel):
    """Esquema para entregar citas"""

    cit_servicio_id: int
    oficina_id: int
    fecha: date
    hora_minuto: time
    notas: Optional[str] = ""


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int
    cit_servicio_id: int
    cit_servicio_descripcion: str
    cit_cliente_id: int
    cit_cliente_nombre: str
    oficina_id: int
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime
    notas: str
    estado: str
    asistencia: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class CitCitaAnonimaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int
    oficina_id: int
    oficina_descripcion_corta: str
    inicio: datetime
    termino: datetime

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
