"""
Domicilios V2, esquemas de pydantic
"""

from pydantic import BaseModel, ConfigDict


class DomicilioOut(BaseModel):
    """Esquema para entregar domicilios"""

    id: int | None = None
    estado: str | None = None
    municipio: str | None = None
    calle: str | None = None
    num_ext: str | None = None
    num_int: str | None = None
    colonia: str | None = None
    cp: int | None = None
    completo: str | None = None
    model_config = ConfigDict(from_attributes=True)
