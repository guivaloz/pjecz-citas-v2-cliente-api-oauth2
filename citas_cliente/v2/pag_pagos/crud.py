"""
Pag Pagos V2, CRUD (create, read, update, and delete)
"""
from datetime import datetime, timedelta
from hashids import Hashids
import re
from typing import Any

from sqlalchemy.orm import Session

from config.settings import LIMITE_CITAS_PENDIENTES, SALT
from lib.safe_string import safe_string, CURP_REGEXP, EMAIL_REGEXP, TELEFONO_REGEXP

from .models import PagPago
from .schemas import PagCarroIn, PagCarroOut, PagResultadoIn, PagResultadoOut
from ..cit_clientes.crud import get_cit_cliente, get_cit_cliente_from_curp, get_cit_cliente_from_email
from ..cit_clientes.models import CitCliente
from ..pag_tramites_servicios.crud import get_pag_tramite_servicio_from_clave

hashids = Hashids(SALT, min_length=8)
hashid_regexp = re.compile("[0-9a-zA-Z]{8,16}")


def get_pag_pagos(
    db: Session,
    cit_cliente_id: int,
    estado: str = None,
) -> Any:
    """Consultar los pagos activos"""

    # Consulta
    consulta = db.query(PagPago)

    # Filtrar por cliente
    cit_cliente = get_cit_cliente(db, cit_cliente_id)
    consulta = consulta.filter(PagPago.cit_cliente == cit_cliente)

    # Filtrar por estado
    if estado is not None:
        estado = safe_string(estado)
        if estado in PagPago.ESTADOS:
            consulta = consulta.filter_by(estado=estado)

    # Entregar
    return consulta.filter_by(estatus="A").order_by(PagPago.id)


def get_pag_pago(
    db: Session,
    pag_pago_id_hasheado: str,
) -> PagPago:
    """Consultar un pago por su id"""

    # Descrifrar el ID hasheado
    if not hashid_regexp.match(pag_pago_id_hasheado):
        raise ValueError("El ID del pago no es válido")
    pag_pago_id = hashids.decode(pag_pago_id_hasheado)[0]

    # Consultar
    pag_pago = db.query(PagPago).get(pag_pago_id)

    # Validar
    if pag_pago is None:
        raise IndexError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")

    # Entregar
    return pag_pago


def create_payment(
    db: Session,
    datos: PagCarroIn,
) -> PagCarroOut:
    """Crear un pago"""

    # Validar nombres
    nombres = safe_string(datos.nombres)
    if nombres == "":
        raise ValueError("El nombre no es valido")

    # Validar apellido_primero
    apellido_primero = safe_string(datos.apellido_primero)
    if apellido_primero == "":
        raise ValueError("El apellido primero no es valido")

    # Validar apellido_segundo
    apellido_segundo = safe_string(datos.apellido_segundo)
    if apellido_segundo == "":
        raise ValueError("El apellido segundo no es valido")

    # Validar curp
    curp = safe_string(datos.curp)
    if re.match(CURP_REGEXP, curp) is None:
        raise ValueError("El CURP no es valido")

    # Validar email
    email = datos.email.strip().lower()
    if re.match(EMAIL_REGEXP, email) is None:
        raise ValueError("El correo electronico no es valido")

    # Validar telefono
    telefono = datos.telefono.strip()
    if re.match(TELEFONO_REGEXP, telefono) is None:
        raise ValueError("El telefono no es valido")

    # Validar pag_tramite_servicio_clave
    pag_tramite_servicio = get_pag_tramite_servicio_from_clave(db, datos.pag_tramite_servicio_clave)

    # Buscar cliente
    cit_cliente = None
    si_existe = False
    try:
        cit_cliente = get_cit_cliente_from_curp(db, curp)
        si_existe = True
    except (IndexError, ValueError):
        try:
            cit_cliente = get_cit_cliente_from_email(db, email)
            si_existe = True
        except (IndexError, ValueError):
            si_existe = False

    # Si no se encuentra el cliente, crearlo
    if not si_existe:
        renovacion_fecha = datetime.now() + timedelta(days=60)
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
            limite_citas_pendientes=LIMITE_CITAS_PENDIENTES,
        )
        db.add(cit_cliente)
        db.commit()
        db.refresh(cit_cliente)
        si_existe = True

    # Insertar pago
    pag_pago = PagPago(
        cit_cliente=cit_cliente,
        pag_tramite_servicio=pag_tramite_servicio,
        estado="SOLICITADO",
        email=email,
        folio="",
        total=pag_tramite_servicio.costo,
        ya_se_envio_comprobante=False,
    )
    db.add(pag_pago)
    db.commit()
    db.refresh(pag_pago)

    # Establecer URL del banco
    url = "https://www.noexiste.com.mx/"

    # Entregar
    return PagCarroOut(
        pag_pago_id=pag_pago.id,
        descripcion=pag_tramite_servicio.descripcion,
        email=email,
        monto=pag_pago.total,
        url=url,
    )


def update_payment(
    db: Session,
    datos: PagResultadoIn,
) -> Any:
    """Actualizar un pago"""

    # Validar el XML que mando el banco
    if datos.xml_encriptado.strip() == "":
        raise ValueError("El XML está vacío")

    # Desencriptar el XML que mando el banco

    # Temporal para probar el front-end
    estado = safe_string(datos.estado)  # Temporal para probar el front-end
    folio = safe_string(datos.folio)  # Temporal para probar el front-end
    pag_pago_id = datos.pag_pago_id  # Temporal para probar el front-end
    if estado not in PagPago.ESTADOS:
        raise ValueError("El estado no es valido")

    # Consultar el pago
    pag_pago = db.query(PagPago).get(pag_pago_id)

    # Validar el pago
    if pag_pago is None:
        raise IndexError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise IndexError("No es activo ese pago, está eliminado")
    if pag_pago.estado != "SOLICITADO":
        raise IndexError("No es un pago solicitado al banco, ya fue procesado")

    # Actualizar el pago
    pag_pago.estado = estado
    pag_pago.folio = folio
    db.add(pag_pago)
    db.commit()
    db.refresh(pag_pago)

    # Entregar
    return PagResultadoOut(
        pag_pago_id=pag_pago.id,
        nombres=pag_pago.cit_cliente.nombres,
        apellido_primero=pag_pago.cit_cliente.apellido_primero,
        apellido_segundo=pag_pago.cit_cliente.apellido_segundo,
        email=pag_pago.email,
        estado=pag_pago.estado,
        folio=pag_pago.folio,
        total=pag_pago.total,
    )
