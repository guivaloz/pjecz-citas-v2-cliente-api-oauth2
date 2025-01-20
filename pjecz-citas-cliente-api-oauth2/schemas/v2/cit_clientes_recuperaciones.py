"""
Cit Clientes Recuperaciones V2, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CitClienteRecuperacionIn(BaseModel):
    """Esquema para recibir al solicitar cambio de contrasena"""

    email: str | None = None
    model_config = ConfigDict(from_attributes=True)


class CitClienteRecuperacionOut(CitClienteRecuperacionIn):
    """Esquema para entregar al solicitar cambio de contrasena"""

    expiracion: datetime
    mensajes_cantidad: int
    ya_recuperado: bool


class CitClienteRecuperacionValidarOut(CitClienteRecuperacionOut):
    """Esquema para entregar al validar que llegue por el URL"""


class CitClienteRecuperacionConcluirIn(BaseModel):
    """Esquema para recibir al concluir el cambio de contrasena"""

    hashid: str
    cadena_validar: str
    password: str


class CitClienteRecuperacionConcluirOut(CitClienteRecuperacionOut):
    """Esquema para entregar al concluir el cambio de contrasena"""
