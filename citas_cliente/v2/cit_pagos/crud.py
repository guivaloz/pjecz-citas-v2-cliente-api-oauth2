"""
Cit Pagos V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
import re
from typing import Any
from sqlalchemy.orm import Session

from lib.safe_string import safe_string, CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP

from .models import CitPago
from ..cit_clientes.models import CitCliente
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_from_email
from ..cit_tramites_servicios.crud import get_cit_tramite_servicio

CANTIDAD_LIMITE = 10


def get_cit_pagos(db: Session, cit_cliente_id: int) -> Any:
    """Consultar los pagos activos"""
    consulta = db.query(CitPago)
    cit_cliente = get_cit_cliente(db, cit_cliente_id=cit_cliente_id)
    consulta = consulta.filter(CitPago.cit_cliente == cit_cliente)
    return consulta.filter_by(estatus="A").order_by(CitPago.id)


def get_cit_pago(db: Session, cit_pago_id: int) -> CitPago:
    """Consultar un pago por su id"""
    cit_pago = db.query(CitPago).get(cit_pago_id)
    if cit_pago is None:
        raise IndexError("No existe ese pago")
    if cit_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")
    return cit_pago


def create_cit_cliente(
    db: Session,
    nombres: str,
    apellido_primero: str,
    apellido_segundo: str,
    curp: str,
    telefono: str,
    email: str,
) -> CitCliente:
    """Crear un cliente para el portal de pagos"""

    # Pasar los datos por las funciones de safe string
    nombres = safe_string(nombres)
    apellido_primero = safe_string(apellido_primero)
    apellido_segundo = safe_string(apellido_segundo)
    curp = safe_string(curp)
    telefono = telefono.strip()

    # Validar nombres
    if nombres == "":
        raise ValueError("El nombre no es valido")

    # Validar apellido primero
    if apellido_primero == "":
        raise ValueError("El apellido primero no es valido")

    # Validar apellido segundo
    if apellido_segundo == "":
        raise ValueError("El apellido segundo no es valido")

    # Validar CURP
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP no es valido")

    # Validar telefono
    if re.match(TELEFONO_REGEXP, telefono) is None:
        raise ValueError("El telefono no es valido")

    # Definir la fecha de renovación dos meses después
    renovacion_fecha = datetime.now() + timedelta(days=60)

    # Insertar el nuevo cliente
    cit_cliente = CitCliente(
        nombres=nombres,
        apellido_primero=apellido_primero,
        apellido_segundo=apellido_segundo,
        curp=curp,
        telefono=telefono,
        email=email,
        contrasena_md5="",
        contrasena_sha256="",
        renovacion=renovacion_fecha.date(),
    )
    db.add(cit_cliente)
    db.commit()
    db.refresh(cit_cliente)

    # Entregar
    return cit_cliente


def create_cit_pago(
    db: Session,
    nombres: str,
    apellido_primero: str,
    apellido_segundo: str,
    curp: str,
    telefono: str,
    email: str,
    cit_tramite_servicio_id: int,
    cantidad: int,
) -> CitPago:
    """Crear un pago"""

    # Validar la cantidad
    if cantidad <= 0 or cantidad > CANTIDAD_LIMITE:
        raise ValueError("No esta la cantidad en el rango permitido")

    # Validar el tramite y servicio
    cit_tramite_servicio = get_cit_tramite_servicio(db, cit_tramite_servicio_id=cit_tramite_servicio_id)  # Causara index error si no existe o esta eliminada

    # Validar email
    email = email.strip().lower()
    if re.match(EMAIL_REGEXP, email) is None:
        raise ValueError("El correo electronico no es valido")

    # Buscar el email en cit_clientes
    try:
        cit_cliente = get_cit_cliente_from_email(db, cliente_email=email)
    except IndexError:
        # No se encontro el email, entonces se va a tratar de agregar un nuevo cliente
        cit_cliente = create_cit_cliente(
            db,
            nombres=nombres,
            apellido_primero=apellido_primero,
            apellido_segundo=apellido_segundo,
            curp=curp,
            telefono=telefono,
            email=email,
        )  # Si falla provoca una excepcion

    # Definir descripcion
    if cantidad == 1:
        descripcion = f"PAGO DE UN(A) {cit_tramite_servicio.nombre}"
    else:
        descripcion = f"PAGO DE {cantidad} {cit_tramite_servicio.nombre}"

    # Defir el total
    total = cantidad * cit_tramite_servicio.costo

    # Insertar el pago
    cit_pago = CitPago(
        cit_cliente=cit_cliente,
        cit_tramite_servicio=cit_tramite_servicio,
        descripcion=descripcion,
        total=total,
        estado="PENDIENTE",
    )
    db.add(cit_pago)
    db.commit()
    db.refresh(cit_pago)

    # Entregar
    return cit_pago


def process_cit_pago(
    db: Session,
    id: int,
    folio: int,
    estado: str,
) -> CitPago:
    """Procesar un pago"""

    # Validar que exista el pago
    cit_pago = get_cit_pago(db, cit_pago_id=id)  # Causara index error si no existe o si esta eliminado

    # Validar que el estado proporcionado no sea PENDIENTE
    if estado == "PENDIENTE":
        raise ValueError("El estado no puede ser PENDIENTE")

    # Validar que el pago tenga el estado PENDIENTE
    if cit_pago.estado != "PENDIENTE":
        raise ValueError("El pago no esta en estado PENDIENTE")

    # Actualizar el registro del pago con el folio y el estado
    cit_pago.folio = folio
    cit_pago.estado = estado
    db.add(cit_pago)
    db.commit()

    # Entregar
    return cit_pago
