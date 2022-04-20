"""
Cit Clientes v1, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class CitClienteOut(BaseModel):
    """Esquema para entregar cliente"""

    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str]
    curp: str
    telefono: Optional[str]
    email: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class CitClienteInDB(CitClienteOut):
    """Cliente en base de datos"""

    username: str
    hashed_password: str
    disabled: bool


class Token(BaseModel):
    """Token"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data"""

    username: Optional[str] = None
