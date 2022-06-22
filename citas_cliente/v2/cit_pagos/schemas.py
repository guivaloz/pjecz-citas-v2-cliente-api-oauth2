"""
Cit Pagos V2, esquemas de pydantic
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CitPagoOut(BaseModel):
    """Esquema para entregar pagos"""

    id: int
    creado: datetime
    cit_cliente_id: int
    cit_cliente_nombre: str
    cit_tramite_servicio_id: int
    cit_tramite_servicio_nombre: str
    descripcion: str
    total: float
    estado: str
    folio: Optional[int] = None

    class Config:
        """SQLAlchemy config"""

        orm_mode = True
