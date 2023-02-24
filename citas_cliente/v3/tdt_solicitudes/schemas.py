"""
Tres de Tres - Solicitudes V3, esquemas de pydantic
"""
from datetime import date, datetime

from pydantic import BaseModel

from lib.schemas_base import OneBaseOut


class TdtSolicitudIn(BaseModel):
    """Esquema para crear una solicitud"""

    cit_cliente_curp: str | None
    cit_cliente_email: str | None
    cit_cliente_nombres: str | None
    cit_cliente_apellido_primero: str | None
    cit_cliente_apellido_segundo: str | None
    cit_cliente_telefono: str | None
    tdt_partido_siglas: str | None
    municipio_id_hasheado: str | None
    cargo: str | None
    principio: str | None
    domicilio_calle: str | None
    domicilio_numero: str | None
    domicilio_colonia: str | None
    domicilio_cp: int | None


class TdtSolicitudOut(TdtSolicitudIn):
    """Esquema para entregar solicitudes"""

    id_hasheado: str | None
    municipio_nombre: str | None
    tdt_partido_nombre: str | None
    creado: datetime | None
    caducidad: date | None
    identificacion_oficial_archivo: str | None
    identificacion_oficial_url: str | None
    comprobante_domicilio_archivo: str | None
    comprobante_domicilio_url: str | None
    autorizacion_archivo: str | None
    autorizacion_url: str | None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True


class OneTdtSolicitudOut(TdtSolicitudOut, OneBaseOut):
    """Esquema para entregar una solicitud"""
