"""
Cit Citas V2, esquemas de pydantic
"""

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict


class CitCitaIn(BaseModel):
    """Esquema para entregar citas"""

    cit_servicio_id: int
    oficina_id: int
    fecha: date
    hora_minuto: time
    notas: str


class CitCitaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int | None = None
    cit_cliente_id: int | None = None
    cit_cliente_nombre: str | None = None
    cit_servicio_id: int | None = None
    cit_servicio_descripcion: str | None = None
    oficina_id: int | None = None
    oficina_descripcion_corta: str | None = None
    inicio: datetime | None = None
    termino: datetime | None = None
    notas: str | None = None
    estado: str | None = None
    asistencia: str | None = None
    codigo_asistencia: str | None = None
    puede_cancelarse: bool | None = None
    model_config = ConfigDict(from_attributes=True)


class CitCitaAnonimaOut(BaseModel):
    """Esquema para entregar citas"""

    id: int | None = None
    oficina_id: int | None = None
    oficina_descripcion_corta: str | None = None
    inicio: datetime | None = None
    termino: datetime | None = None
    model_config = ConfigDict(from_attributes=True)
