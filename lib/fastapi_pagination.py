"""
FastAPI Pagination
"""
from typing import TypeVar, Generic
from fastapi import Query
from fastapi_pagination.default import Page as BasePage, Params as BaseParams
from fastapi_pagination.limit_offset import LimitOffsetPage as BaseLimitOffsetPage, LimitOffsetParams as BaseLimitOffsetParams

LIMIT_DEFAULT = 100
LIMIT_MAX = 1000
T = TypeVar("T")


class LimitOffsetParams(BaseLimitOffsetParams):
    """Ajuste para que LimitOffsetPage"""

    limit: int = Query(LIMIT_DEFAULT, ge=1, le=LIMIT_MAX, description="Page size limit")
    offset: int = Query(0, ge=0, description="Page offset")


class LimitOffsetPage(BaseLimitOffsetPage[T], Generic[T]):
    """Definir nuevos parametros por defecto"""

    __params_type__ = LimitOffsetParams


class PageParams(BaseParams):
    """Ajuste para que Page"""

    size: int = Query(LIMIT_DEFAULT, ge=1, le=LIMIT_MAX, description="Page size")


class Page(BasePage[T], Generic[T]):
    """Definir nuevos parametros por defecto"""

    __params_type__ = PageParams
