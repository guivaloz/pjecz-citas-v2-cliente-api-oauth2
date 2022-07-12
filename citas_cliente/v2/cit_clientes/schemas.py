"""
Cit Clientes V2, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class CitClienteOut(BaseModel):
    """Esquema para entregar cliente"""

    id: int
    nombres: str
    apellido_primero: str
    apellido_segundo: Optional[str]
    curp: str
    telefono: Optional[str]
    email: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class CitClienteInDB(CitClienteOut):
    """Cliente en base de datos"""

    username: str
    permissions: dict
    hashed_password: str
    disabled: bool


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str
    username: str


class TokenData(BaseModel):
    """Token data"""

    username: Optional[str] = None


class CitClienteActualizarContrasenaIn(BaseModel):
    """Esquema para recibir la actualizacion de la contrasena"""

    email: str
    contrasena_anterior: str
    contrasena_nueva: str


class CitClienteActualizarContrasenaOut(CitClienteOut):
    """Esquema para entregar los datos del cliente y el mensaje de la actualizacion de la contrasena"""

    mensaje: str
