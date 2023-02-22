"""
Pago de Pensiones Alimenticias - Solicitudes, modelos
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class PpaSolicitud(Base, UniversalMixin):
    """PpaSolicitud"""

    # Nombre de la tabla
    __tablename__ = "ppa_solicitudes"

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

    @property
    def autoridad_clave(self):
        """Autoridad clave"""
        return self.autoridad.clave

    @property
    def autoridad_descripcion(self):
        """Autoridad descripción"""
        return self.autoridad.descripcion

    @property
    def autoridad_descripcion_corta(self):
        """Autoridad descripción corta"""
        return self.autoridad.descripcion_corta

    @property
    def cit_cliente_curp(self):
        """CURP del cliente"""
        return self.cit_cliente.curp

    @property
    def cit_cliente_email(self):
        """e-mail del cliente"""
        return self.cit_cliente.email

    @property
    def cit_cliente_nombres(self):
        """Nombres del cliente"""
        return self.cit_cliente.nombres

    @property
    def cit_cliente_apellido_primero(self):
        """Apellido primero del cliente"""
        return self.cit_cliente.apellido_primero

    @property
    def cit_cliente_apellido_segundo(self):
        """Apellido segundo del cliente"""
        return self.cit_cliente.apellido_segundo

    @property
    def distrito_nombre(self):
        """Nombre del distrito"""
        return self.autoridad.distrito.nombre

    def __repr__(self):
        """Representación"""
        return f"<PpaSolicitud {self.id}>"
