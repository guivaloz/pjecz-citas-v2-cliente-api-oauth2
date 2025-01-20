"""
Encuestas Servicios V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


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
    respuesta_01: int
    respuesta_02: int
    respuesta_03: int
    respuesta_04: str
    estado: str
    model_config = ConfigDict(from_attributes=True)


class EncServicioURLOut(BaseModel):
    """Esquema para entregar una URL de encuesta de servicio"""

    url: str | None = None
