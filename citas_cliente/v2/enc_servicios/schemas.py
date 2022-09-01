"""
Encuestas Servicios V2, esquemas de pydantic
"""
from typing import Optional
from pydantic import BaseModel


class EncServicioIn(BaseModel):
    """Esquema para recibir una encuesta de servicio"""

    hashid: str
    respuesta_01: int
    respuesta_02: int
    respuesta_03: int
    respuesta_04: str


class EncServicioOut(EncServicioIn):
    """Esquema para entregar una encuesta de servicio"""

    id: int
    cit_cliente_id: int
    cit_cliente_email: str
    cit_cliente_nombre: str
    oficina_id: int
    oficina_clave: str
    oficina_descripcion: str
    oficina_descripcion_corta: str
    respuesta_01: Optional[int] = None
    respuesta_02: Optional[int] = None
    respuesta_03: Optional[int] = None
    respuesta_04: Optional[str] = ""
    estado: str

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
