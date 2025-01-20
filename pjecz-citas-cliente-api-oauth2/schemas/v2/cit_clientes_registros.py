"""
Cit Clientes Registros V2, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CitClienteRegistroIn(BaseModel):
    """Esquema para recibir al solicitar una nueva cuenta"""

    nombres: str
    apellido_primero: str
    apellido_segundo: str
    curp: str
    telefono: str
    email: str
    model_config = ConfigDict(from_attributes=True)


class CitClienteRegistroOut(CitClienteRegistroIn):
    """Esquema para entregar al solicitar una nueva cuenta"""

    expiracion: datetime | None = None
    mensajes_cantidad: int | None = None
    ya_registrado: bool | None = None


class CitClienteRegistroValidarOut(CitClienteRegistroOut):
    """Esquema para entregar al validar que llegue por el URL"""


class CitClienteRegistroConcluirIn(BaseModel):
    """Esquema para recibir al concluir la nueva cuenta"""

    hashid: str
    cadena_validar: str
    password: str


class CitClienteRegistroConcluirOut(CitClienteRegistroOut):
    """Esquema para entregar al concluir la nueva cuenta"""
