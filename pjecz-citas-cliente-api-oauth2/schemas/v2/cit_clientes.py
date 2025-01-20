"""
Cit Clientes V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class CitClienteOut(BaseModel):
    """Esquema para entregar cliente"""

    id: int | None = None
    nombres: str | None = None
    apellido_primero: str | None = None
    apellido_segundo: str | None = None
    curp: str | None = None
    telefono: str | None = None
    email: str | None = None
    limite_citas_pendientes: int | None = None
    autoriza_mensajes: bool | None = None
    enviar_boletin: bool | None = None
    model_config = ConfigDict(from_attributes=True)


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

    username: str


class CitClienteActualizarContrasenaIn(BaseModel):
    """Esquema para recibir la actualizacion de la contrasena"""

    email: str
    contrasena_anterior: str
    contrasena_nueva: str


class CitClienteActualizarContrasenaOut(CitClienteOut):
    """Esquema para entregar los datos del cliente y el mensaje de la actualizacion de la contrasena"""

    mensaje: str
