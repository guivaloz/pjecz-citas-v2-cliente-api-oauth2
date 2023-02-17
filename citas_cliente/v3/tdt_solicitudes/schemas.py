"""
Tres de Tres - Solicitudes V3, esquemas de pydantic
"""
from datetime import datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class TdtSolicitudOut(BaseModel):
    """Esquema para entregar solicitudes"""

    id: int | None
    cit_cliente_email: str | None
    cit_cliente_nombre: str | None
    municipio_nombre: str | None
    tdt_partido_siglas: str | None
    tdt_partido_nombre: str | None
    cargo: str | None
    principio: str | None
    domicilio_calle: str | None
    domicilio_numero: str | None
    domicilio_colonia: str | None
    domicilio_cp: int | None
    identificacion_oficial_archivo: str | None
    identificacion_oficial_url: str | None
    comprobante_domicilio_archivo: str | None
    comprobante_domicilio_url: str | None
    autorizacion_archivo: str | None
    autorizacion_url: str | None
    ya_se_envio_acuse: bool | None
    creado: datetime | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneTdtSolicitudOut(TdtSolicitudOut, OneBaseOut):
    """Esquema para entregar una solicitud"""
