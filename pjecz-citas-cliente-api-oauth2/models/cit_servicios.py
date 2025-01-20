"""
Cit Servicios, modelos
"""

from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitServicio(Base, UniversalMixin):
    """CitServicio"""

    # Nombre de la tabla
    __tablename__ = "cit_servicios"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_categoria_id = Column(Integer, ForeignKey("cit_categorias.id"), index=True, nullable=False)
    cit_categoria = relationship("CitCategoria", back_populates="cit_servicios")

    # Columnas
    clave = Column(String(32), unique=True, nullable=False)
    descripcion = Column(String(64), nullable=False)
    duracion = Column(Time(), nullable=False)
    documentos_limite = Column(Integer, nullable=False)
    desde = Column(Time(), nullable=True)
    hasta = Column(Time(), nullable=True)
    dias_habilitados = Column(String(7), nullable=False)

    # Hijos
    cit_citas = relationship("CitCita", back_populates="cit_servicio")
    cit_oficinas_servicios = relationship("CitOficinaServicio", back_populates="cit_servicio")

    @property
    def cit_categoria_nombre(self):
        """Nombre de la categoria"""
        return self.cit_categoria.nombre

    def __repr__(self):
        """Representación"""
        return f"<CitServicio {self.clave}>"
