"""
Pago de Pensiones Alimenticias - Solicitudes V2, modelos
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class PpaSolicitud(Base, UniversalMixin):
    """PpaSolicitud"""

    # Nombre de la tabla
    __tablename__ = "ppa_slicitudes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    autoridad_id = Column(Integer, ForeignKey("autoridades.id"), index=True, nullable=False)
    autoridad = relationship("Autoridad", back_populates="ppa_solicitudes")
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="ppa_solicitudes")

    # Columnas domicilio particular
    domicilio_calle = Column(String(256))
    domicilio_numero = Column(String(24))
    domicilio_colonia = Column(String(256))
    domicilio_cp = Column(Integer())

    # Columnas compañía telefónica
    compania_telefonica = Column(String(64))

    # Columnas número de expediente donde se decretó la pensión
    numero_expediente = Column(String(24))

    # Columnas archivo PDF de la credencial de elector
    identificacion_oficial_archivo = Column(String(64))
    identificacion_oficial_url = Column(String(256))

    # Columnas archivo PDF del comprobante de domicilio
    comprobante_domicilio_archivo = Column(String(64))
    comprobante_domicilio_url = Column(String(256))

    # Columnas archivo PDF de la autorización de transferencia de datos personales
    autorizacion_archivo = Column(String(64))
    autorizacion_url = Column(String(256))

    # Columnas mensajes
    ya_se_envio_acuse = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        """Representación"""
        return f"<PpaSolicitud {self.id}>"
