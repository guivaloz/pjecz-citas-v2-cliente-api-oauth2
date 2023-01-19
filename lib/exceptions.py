"""
Exceptions
"""


class CitasAnyError(Exception):
    """Base exception class"""


class CitasAlreadyExistsError(CitasAnyError):
    """Excepción porque ya existe"""


class CitasAuthenticationError(CitasAnyError):
    """Excepción porque fallo la autentificacion"""


class CitasConnectionError(CitasAnyError):
    """Excepción porque no se pudo conectar"""


class CitasEmptyError(CitasAnyError):
    """Excepción porque no hay resultados"""


class CitasIsDeletedError(CitasAnyError):
    """Excepción porque esta eliminado"""


class CitasMissingConfigurationError(CitasAnyError):
    """Excepción porque falta configuración"""


class CitasNotExistsError(CitasAnyError):
    """Excepción porque no existe"""


class CitasNotValidParamError(CitasAnyError):
    """Excepción porque un parámetro es inválido"""


class CitasOutOfRangeParamError(CitasAnyError):
    """Excepción porque un parámetro esta fuera de rango"""


class CitasRequestError(CitasAnyError):
    """Excepción porque falló el request"""


class CitasTimeoutError(CitasAnyError):
    """Excepción porque se agoto el tiempo de espera"""
