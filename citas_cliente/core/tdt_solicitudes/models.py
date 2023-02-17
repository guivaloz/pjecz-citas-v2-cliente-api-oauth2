"""
Tres de Tres - Solicitudes, modelos
"""
from collections import OrderedDict
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from lib.database import Base
from lib.universal_mixin import UniversalMixin


class TdtSolicitud(Base, UniversalMixin):
    """TdtSolicitud"""

    CARGOS = OrderedDict(
        [
            ("GOBERNATURA", "Gobernatura"),
            ("PRESIDENCIA MUNICIPAL", "Presidencia Municipal"),
            ("REGIDURIA", "Regiduría"),
            ("SINDICATURA", "Sindicatura"),
        ]
    )

    PRINCIPIOS = OrderedDict(
        [
            ("MAYORIA RELATIVA", "Mayoría relativa"),
            ("REPRESENTACION PROPORCIONAL", "Representación proporcional"),
        ]
    )

    # Nombre de la tabla
    __tablename__ = "tdt_solicitudes"

    # Clave primaria
    id = Column(Integer, primary_key=True)

    # Claves foráneas
    cit_cliente_id = Column(Integer, ForeignKey("cit_clientes.id"), index=True, nullable=False)
    cit_cliente = relationship("CitCliente", back_populates="tdt_solicitudes")
    municipio_id = Column(Integer, ForeignKey("municipios.id"), index=True, nullable=False)
    municipio = relationship("Municipio", back_populates="tdt_solicitudes")
    tdt_partido_id = Column(Integer, ForeignKey("tdt_partidos.id"), index=True, nullable=False)
    tdt_partido = relationship("TdtPartido", back_populates="tdt_solicitudes")

    # Columnas cargo y principio
    cargo = Column(Enum(*CARGOS, name="tdt_solicitudes_tipos_cargos", native_enum=False), index=True, nullable=False)
    principio = Column(Enum(*PRINCIPIOS, name="tdt_solicitudes_tipos_principios", native_enum=False), index=True, nullable=False)

    # Columnas domicilio particular
    domicilio_calle = Column(String(256))
    domicilio_numero = Column(String(24))
    domicilio_colonia = Column(String(256))
    domicilio_cp = Column(Integer())

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
    def municipio_nombre(self):
        """Nombre del municipio"""
        return self.municipio.nombre

    @property
    def tdt_partido_nombre(self):
        """Nombre del partido"""
        return self.tdt_partido.nombre

    @property
    def tdt_partido_siglas(self):
        """Siglas del partido"""
        return self.tdt_partido.siglas

    def __repr__(self):
        """Representación"""
        return f"<TdtSolicitud {self.descripcion}>"
