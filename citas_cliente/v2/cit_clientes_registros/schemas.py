"""
Cit Clientes Registros V2, esquemas de pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CitClienteRegistroIn(BaseModel):
    """Esquema para recibir al solicitar una nueva cuenta"""

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
    """Esquema para entregar al solicitar una nueva cuenta"""

    expiracion: datetime
    mensajes_cantidad: int
    ya_registrado: bool


class CitClienteRegistroValidarOut(CitClienteRegistroOut):
    """Esquema para entregar al validar que llegue por el URL"""


class CitClienteRegistroConcluirIn(BaseModel):
    """Esquema para recibir al concluir la nueva cuenta"""

    hashid: str
    cadena_validar: str
    password: str


class CitClienteRegistroConcluirOut(CitClienteRegistroOut):
    """Esquema para entregar al concluir la nueva cuenta"""
