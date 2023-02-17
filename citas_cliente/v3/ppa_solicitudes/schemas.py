"""
Pago de Pensiones Alimenticias - Solicitudes V3, esquemas de pydantic
"""
from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PpaSolicitudOut(BaseModel):
    """Esquema para entregar solicitudes"""

    id: int | None
    autoridad_clave: int | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    cit_cliente_email: str | None
    cit_cliente_nombre: str | None
    distrito_nombre: str | None
    domicilio_calle: str | None
    domicilio_numero: str | None
    domicilio_colonia: str | None
    domicilio_cp: int | None
    compania_telefonica: str | None
    numero_expediente: str | None
    identificacion_oficial_archivo: str | None
    identificacion_oficial_url: str | None
    comprobante_domicilio_archivo: str | None
    comprobante_domicilio_url: str | None
    autorizacion_archivo: str | None
    autorizacion_url: str | None
    ya_se_envio_acuse: bool | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePpaSolicitudOut(PpaSolicitudOut, OneBaseOut):
    """Esquema para entregar una solicitud"""
