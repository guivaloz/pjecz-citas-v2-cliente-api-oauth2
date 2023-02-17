"""
Pago de Pensiones Alimenticias - Solicitudes V3, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class PpaSolicitudIn(BaseModel):
    """Esquema para crear una solicitud"""

    autoridad_clave: str | None
    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    cit_cliente_nombres: str | None
    cit_cliente_apellido_primero: str | None
    cit_cliente_apellido_segundo: str | None
    cit_cliente_telefono: str | None
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


class PpaSolicitudOut(PpaSolicitudIn):
    """Esquema para entregar solicitudes"""

    id: int | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    distrito_nombre: str | None
    ya_se_envio_acuse: bool | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OnePpaSolicitudOut(PpaSolicitudOut, OneBaseOut):
    """Esquema para entregar una solicitud"""
