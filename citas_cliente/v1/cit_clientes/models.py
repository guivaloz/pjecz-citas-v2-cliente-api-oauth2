"""
Cit Clientes v1, modelos
"""
from datetime import datetime
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitCliente(Base, UniversalMixin):
    """CitCliente"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Columnas
    nombres = Column(String(256), nullable=False)
    apellido_paterno = Column(String(256), nullable=False)
    apellido_materno = Column(String(256))
    curp = Column(String(18), unique=True, nullable=False)
    telefono = Column(String(64))
    email = Column(String(256), unique=True, nullable=False)
    contrasena = Column(String(256), nullable=False)
    hash = Column(String(256))
    renovacion_fecha = Column(Date(), nullable=False)

    @property
    def nombre(self):
        """Junta nombres, apellido_paterno y apellido materno"""
        return self.nombres + " " + self.apellido_paterno + " " + self.apellido_materno

    @property
    def permissions(self):
        """Entrega un diccionario con todos los permisos si no ha llegado la fecha de renovación"""
        if self.renovacion_fecha < datetime.now().date():
            return {}
        # Los permisos son fijos para todos los clientes
        return {
            "AUTORIDADES": 1,
            "DISTRITOS": 1,
            "MATERIAS": 1,
        }

    def __repr__(self):
        """Representación"""
        return f"<CitCliente {self.email}>"
