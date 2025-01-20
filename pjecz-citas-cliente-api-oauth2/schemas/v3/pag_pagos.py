"""
Pagos Pagos V3, esquemas de pydantic
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ...dependencies.schemas_base import OneBaseOut


class PagPagoOut(BaseModel):
    """Esquema para entregar pagos"""

    id_hasheado: str | None
    autoridad_descripcion: str | None
    cantidad: int | None
    cit_cliente_nombre: str | None
    descripcion: str | None
    distrito_nombre: str | None
    email: str | None
    estado: str | None
    folio: str | None
    pag_tramite_servicio_descripcion: str | None
    resultado_tiempo: datetime | None
    total: float | None
    model_config = ConfigDict(from_attributes=True)


class OnePagPagoOut(PagPagoOut, OneBaseOut):
    """Esquema para entregar un pago"""


class PagCarroIn(BaseModel):
    """Esquema para recibir del carro de pagos"""

    apellido_primero: str | None
    apellido_segundo: str | None
    autoridad_clave: str | None
    cantidad: int | None
    curp: str | None
    descripcion: str | None
    distrito_clave: str | None
    email: str | None
    nombres: str | None
    pag_tramite_servicio_clave: str | None
    telefono: str | None


class PagCarroOut(BaseModel):
    """Esquema para entregar al carro de pagos"""

    id_hasheado: str | None
    autoridad_clave: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    cantidad: int | None
    descripcion: str | None
    distrito_clave: str | None
    distrito_nombre: str | None
    distrito_nombre_corto: str | None
    email: str | None
    total: float | None
    url: str | None


class OnePagCarroOut(PagCarroOut, OneBaseOut):
    """Esquema para entregar un pago"""


class PagResultadoIn(BaseModel):
    """Esquema para recibir del carro de pagos"""

    xml_encriptado: str | None


class PagResultadoOut(BaseModel):
    """Esquema para entregar al carro de pagos"""

    id_hasheado: str | None
    autoridad_clave: str | None
    autoridad_descripcion: str | None
    autoridad_descripcion_corta: str | None
    cantidad: int | None
    nombres: str | None
    apellido_primero: str | None
    apellido_segundo: str | None
    email: str | None
    estado: str | None
    folio: str | None
    resultado_tiempo: datetime | None
    total: float | None


class OnePagResultadoOut(PagResultadoOut, OneBaseOut):
    """Esquema para entregar un pago"""
