"""
Cit Clientes Registros v1, esquemas de pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CitClienteRegistroIn(BaseModel):
    """Esquema para entregar registros de clientes"""

    nombres: str
    apellido_primero: str
    apellido_segundo: Optional[str] = ""
    curp: str
    telefono: str
    email: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class CitClienteRegistroOut(CitClienteRegistroIn):
    """Esquema para entregar registros de clientes"""

    expiracion: datetime
