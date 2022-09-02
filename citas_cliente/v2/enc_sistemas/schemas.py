"""
Encuestas Sistemas V2, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class EncSistemaIn(BaseModel):
    """Esquema para entregar encuesta de sistema"""

    hashid: str
    respuesta_01: int
    respuesta_02: str
    respuesta_03: str


class EncSistemaOut(EncSistemaIn):
    """Esquema para entregar encuesta de sistema"""

    id: int
    cit_cliente_id: int
    cit_cliente_email: str
    cit_cliente_nombre: str
    respuesta_01: Optional[int] = None
    respuesta_02: Optional[str] = ""
    respuesta_03: Optional[str] = ""
    estado: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
