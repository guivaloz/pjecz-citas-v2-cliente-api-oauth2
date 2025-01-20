"""
Cit Categorias, modelos
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitCategoria(Base, UniversalMixin):
    """CitCategoria"""

    # Nombre de la tabla
    __tablename__ = "cit_categorias"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(64), unique=True, nullable=False)

    # Hijos
    cit_servicios = relationship("CitServicio", back_populates="cit_categoria")

    def __repr__(self):
        """Representación"""
        return f"<CitCategoria {self.nombre}>"
