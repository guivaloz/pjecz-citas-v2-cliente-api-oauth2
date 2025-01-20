"""
Cit Categorias V2, CRUD (create, read, update, and delete)
"""

from typing import Any

from sqlalchemy.orm import Session

from ...models.cit_categorias import CitCategoria


def get_cit_categorias(db: Session) -> Any:
    """Consultar las catagorias activas"""
    return db.query(CitCategoria).filter_by(estatus="A").order_by(CitCategoria.id)


def get_cit_categoria(db: Session, cit_categoria_id: int) -> CitCategoria:
    """Consultar una categoria por su id"""
    cit_categoria = db.query(CitCategoria).get(cit_categoria_id)
    if cit_categoria is None:
        raise IndexError("No existe ese categoria")
    if cit_categoria.estatus != "A":
        raise IndexError("No es activo ese categoria, está eliminado")
    return cit_categoria
