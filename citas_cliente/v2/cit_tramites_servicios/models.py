"""
Cit Tramites Servicios V2, modelos
"""
from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitTramiteServicio(Base, UniversalMixin):
    """CitTramiteServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_tramites_servicios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombre = Column(String(256), nullable=False, unique=True)
    costo = Column(Numeric(12, 2), nullable=False)
    url = Column(String(512), nullable=False)

    # Hijos
    cit_pagos = relationship("CitPago", back_populates="cit_tramite_servicio")

    def __repr__(self):
        """Representación"""
        return f"<CitTramiteServicio {self.nombre}>"
