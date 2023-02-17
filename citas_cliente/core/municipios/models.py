"""
Municipios, modelos
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class Municipio(Base, UniversalMixin):
    """Municipio"""

    # Nombre de la tabla
    __tablename__ = "municipios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), unique=True, nullable=False)

    # Hijos
    tdt_solicitudes = relationship("TdtSolicitud", back_populates="municipio")

    def __repr__(self):
        """Representación"""
        return f"<Municipio {self.nombre}>"
