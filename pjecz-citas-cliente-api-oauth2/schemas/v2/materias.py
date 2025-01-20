"""
Materias V2, esquemas
"""

from pydantic import BaseModel, ConfigDict


class MateriaOut(BaseModel):
    """Esquema para entregar materia"""

    id: int | None = None
    nombre: str | None = None
    model_config = ConfigDict(from_attributes=True)
