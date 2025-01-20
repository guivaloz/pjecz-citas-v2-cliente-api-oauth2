"""
Encuestas Sistemas V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class EncSistemaIn(BaseModel):
    """Esquema para entregar encuesta de sistema"""

    hashid: str
    respuesta_01: int
    respuesta_02: str
    respuesta_03: str


class EncSistemaOut(EncSistemaIn):
    """Esquema para entregar encuesta de sistema"""

    id: int | None = None
    cit_cliente_id: int | None = None
    cit_cliente_email: str | None = None
    cit_cliente_nombre: str | None = None
    respuesta_01: int | None = None
    respuesta_02: str | None = None
    respuesta_03: str | None = None
    estado: str | None = None
    model_config = ConfigDict(from_attributes=True)


class EncSistemaURLOut(BaseModel):
    """Esquema para entregar una URL de encuesta de servicio"""

    url: str | None = None
