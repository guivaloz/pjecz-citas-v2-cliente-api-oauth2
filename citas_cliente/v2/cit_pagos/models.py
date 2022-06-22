"""
Cit Pagos V2, modelos
"""
from collections import OrderedDict
from sqlalchemy import Column, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class CitPago(Base, UniversalMixin):
    """CitPago"""

    ESTADOS = OrderedDict(
        [
            ("PENDIENTE", "Pendiente"),
            ("REALIZADO", "Realizado"),
            ("CANCELADO", "Cancelado"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "cit_pagos"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Clave foránea
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="cit_pagos")
    cit_tramite_servicio_id = Column(Integer, ForeignKey("cit_tramites_servicios.id"), index=True, nullable=False)
    cit_tramite_servicio = relationship("CitTramiteServicio", back_populates="cit_pagos")

    # Columnas
    descripcion = Column(String(256), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    estado = Column(Enum(*ESTADOS, name="estados", native_enum=False))
    folio = Column(Integer())

    @property
    def cit_cliente_nombre(self):
        """Nombre del cliente"""
        return self.cit_cliente.nombre

    @property
    def cit_tramite_servicio_nombre(self):
        """Nombre del tramite y servicio"""
        return self.cit_tramite_servicio.nombre

    def __repr__(self):
        """Representación"""
        return f"<CitPago {self.descripcion} ${self.total}>"
