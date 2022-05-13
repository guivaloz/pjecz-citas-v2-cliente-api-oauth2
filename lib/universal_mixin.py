"""
UniversalMixin define las columnas y métodos comunes de todos los modelos
"""
from sqlalchemy import Column, DateTime, String
from sqlalchemy.sql import func


class UniversalMixin:
    """Columnas y métodos comunes a todas las tablas"""

    creado = Column(DateTime, server_default=func.now(), nullable=False)
    modificado = Column(DateTime, onupdate=func.now(), server_default=func.now())
    estatus = Column(String(1), server_default="A", nullable=False)
