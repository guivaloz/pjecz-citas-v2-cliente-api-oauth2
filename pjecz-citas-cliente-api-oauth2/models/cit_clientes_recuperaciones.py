"""
Cit Clientes Recuperaciones, modelos
"""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base
from ..dependencies.universal_mixin import UniversalMixin


class CitClienteRecuperacion(Base, UniversalMixin):
    """CitClienteRecuperacion"""

    # Nombre de la tabla
    __tablename__ = "cit_clientes_recuperaciones"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="cit_clientes_recuperaciones")

    # Columnas
    expiracion = Column(DateTime(), nullable=False)
    cadena_validar = Column(String(256), nullable=False)
    mensajes_cantidad = Column(Integer(), nullable=False, default=0)
    ya_recuperado = Column(Boolean(), default=False)

    @property
    def cit_cliente_email(self):
        """Retorna el email del cliente"""
        return self.cit_cliente.email

    @property
    def email(self):
        """Retorna el email del cliente"""
        return self.cit_cliente.email

    def __repr__(self):
        """Representación"""
        return f"<CitClienteRecuperacion {self.id}>"
