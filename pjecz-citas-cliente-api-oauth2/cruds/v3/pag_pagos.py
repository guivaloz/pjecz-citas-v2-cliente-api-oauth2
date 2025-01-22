"""
Pagos Pagos V3, CRUD (create, read, update, and delete)
"""

from datetime import datetime, timedelta
from typing import Any

import nest_asyncio
from sqlalchemy.orm import Session

from ...dependencies.exceptions import CitasAnyError, CitasIsDeletedError, CitasNotExistsError, CitasNotValidParamError
from ...dependencies.hashids import cifrar_id, descifrar_id
from ...dependencies.safe_string import safe_curp, safe_email, safe_integer, safe_string, safe_telefono
from ...dependencies.santander_web_pay_plus import RESPUESTA_EXITO, convert_xml_to_dict, create_pay_link, decrypt_chain
from ...models.cit_clientes import CitCliente
from ...models.pag_pagos import PagPago
from ...schemas.v3.pag_pagos import PagCarroIn, PagCarroOut, PagResultadoIn, PagResultadoOut
from ...settings import LIMITE_CITAS_PENDIENTES, LOCAL_HUSO_HORARIO
from .autoridades import get_autoridad_from_clave
from .cit_clientes import get_cit_cliente, get_cit_cliente_from_curp, get_cit_cliente_from_email
from .distritos import get_distrito_from_clave, get_distrito_from_nombre
from .pag_tramites_servicios import get_pag_tramite_servicio_from_clave


def get_pag_pagos(db: Session, cit_cliente_id: int, estado: str = None) -> Any:
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
    return consulta.filter_by(estatus="A").order_by(PagPago.id.desc())


def get_pag_pago(db: Session, pag_pago_id: int) -> PagPago:
    """Consultar un pago por su id"""
    pag_pago = db.query(PagPago).get(pag_pago_id)
    if pag_pago is None:
        raise CitasNotExistsError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise CitasIsDeletedError("No es activo ese pago, está eliminado")
    return pag_pago


def get_pag_pago_from_id_hasheado(db: Session, pag_pago_id_hasheado: str) -> PagPago:
    """Consultar un pago por su id hasheado"""
    pag_pago_id = descifrar_id(pag_pago_id_hasheado)
    if pag_pago_id is None:
        raise CitasNotValidParamError("El ID del pago no es válido")
    return get_pag_pago(db, pag_pago_id)


def create_payment(
    db: Session,
    datos: PagCarroIn,
) -> PagCarroOut:
    """Crear un pago"""

    # Validar nombres
    nombres = safe_string(datos.nombres, save_enie=True)
    if nombres == "":
        raise CitasNotValidParamError("El nombre no es valido")

    # Validar apellido_primero
    apellido_primero = safe_string(datos.apellido_primero, save_enie=True)
    if apellido_primero == "":
        raise CitasNotValidParamError("El apellido primero no es valido")

    # Validar apellido_segundo
    apellido_segundo = safe_string(datos.apellido_segundo, save_enie=True)
    if apellido_segundo == "":
        raise CitasNotValidParamError("El apellido segundo no es valido")

    # Validar curp
    try:
        curp = safe_curp(datos.curp)
    except ValueError as error:
        raise CitasNotValidParamError("La CURP no es valida") from error

    # Validar email
    try:
        email = safe_email(datos.email)
    except ValueError as error:
        raise CitasNotValidParamError("El email no es valido") from error

    # Validar telefono
    try:
        telefono = safe_telefono(datos.telefono)
    except ValueError as error:
        raise CitasNotValidParamError("El telefono no es valido") from error

    # Validar pag_tramite_servicio_clave
    pag_tramite_servicio = get_pag_tramite_servicio_from_clave(db, datos.pag_tramite_servicio_clave)

    # Puede venir la clave de la autoridad
    try:
        autoridad = get_autoridad_from_clave(db, datos.autoridad_clave)
    except CitasAnyError as error:
        autoridad = get_autoridad_from_clave(db, "ND")  # Autoridad NO DEFINIDO

    # Puede venir la cantidad
    cantidad = safe_integer(datos.cantidad, default=1)  # Por defecto es 1

    # Puede venir la descripcion
    descripcion = pag_tramite_servicio.descripcion  # Por defecto es la descripcion del tramite-servicio
    descripcion_adicional = safe_string(datos.descripcion, save_enie=True)
    if descripcion_adicional != "":
        descripcion = safe_string(f"{descripcion} - {descripcion_adicional}", save_enie=True)

    # Puede venir la clave del distrito
    distrito = autoridad.distrito  # Por defecto es el distrito de la autoridad
    if datos.distrito_clave is not None and datos.distrito_clave != "":
        try:
            distrito = get_distrito_from_clave(db, datos.distrito_clave)
        except CitasAnyError as error:
            distrito = autoridad.distrito  # Por defecto es el distrito de la autoridad

    # Calcular el total que es el costo del tramite-servicio por la cantidad
    total = pag_tramite_servicio.costo * cantidad

    # Validar que el total sea mayor a cero
    if total <= 0:
        raise CitasNotValidParamError("El total no es valido")

    # Buscar cliente
    cit_cliente = None
    si_existe = False
    try:
        cit_cliente = get_cit_cliente_from_curp(db, curp)
        si_existe = True
    except CitasAnyError:
        try:
            cit_cliente = get_cit_cliente_from_email(db, email)
            si_existe = True
        except CitasAnyError:
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

    # Definir la fecha de caducidad que sea dentro de 30 días
    caducidad = datetime.now() + timedelta(days=30)

    # Insertar pago
    pag_pago = PagPago(
        autoridad=autoridad,
        distrito=distrito,
        cit_cliente=cit_cliente,
        pag_tramite_servicio=pag_tramite_servicio,
        caducidad=caducidad.date(),
        cantidad=cantidad,
        descripcion=descripcion,
        email=email,
        estado="SOLICITADO",
        total=total,
        ya_se_envio_comprobante=False,
    )
    db.add(pag_pago)
    db.commit()
    db.refresh(pag_pago)

    # Crear URL al banco
    nest_asyncio.apply()
    try:
        url = create_pay_link(
            pago_id=pag_pago.id,
            email=email,
            service_detail=pag_tramite_servicio.descripcion,
            cit_client_id=cit_cliente.id,
            amount=float(total),
        )
    except CitasAnyError as error:
        raise error

    # Entregar
    return PagCarroOut(
        id_hasheado=cifrar_id(pag_pago.id),
        autoridad_clave=autoridad.clave,
        autoridad_descripcion=autoridad.descripcion,
        autoridad_descripcion_corta=autoridad.descripcion_corta,
        cantidad=cantidad,
        descripcion=descripcion,
        distrito_clave=distrito.clave,
        distrito_nombre=distrito.nombre,
        distrito_nombre_corto=distrito.nombre_corto,
        email=email,
        total=total,
        url=url,
    )


def update_payment(
    db: Session,
    datos: PagResultadoIn,
) -> PagResultadoOut:
    """Actualizar un pago, ahora puede guardar el contenido XML del banco"""

    # Validar el XML que mando el banco
    if datos.xml_encriptado.strip() == "":
        raise CitasNotValidParamError("El XML está vacío")

    # Desencriptar el XML que mando el banco
    try:
        respuesta_xml = decrypt_chain(datos.xml_encriptado)
        respuesta = convert_xml_to_dict(respuesta_xml)
    except CitasAnyError as error:
        raise error

    # Consultar el pago
    pag_pago_id = int(respuesta["pago_id"])
    pag_pago = db.query(PagPago).get(pag_pago_id)

    # Validar el pago
    if pag_pago is None:
        raise CitasNotExistsError("No existe ese pago")
    if pag_pago.estatus != "A":
        raise CitasIsDeletedError("No es activo ese pago, está eliminado")
    if pag_pago.estado != "SOLICITADO":
        raise CitasNotExistsError("No es un pago solicitado al banco, ya fue procesado")

    # Definir el estado, puede ser PAGADO o FALLIDO
    estado = "PAGADO" if respuesta["respuesta"] == RESPUESTA_EXITO else "FALLIDO"
    if estado not in PagPago.ESTADOS:
        raise CitasNotValidParamError("El estado no es valido")

    # Actualizar el pago
    pag_pago.estado = estado
    pag_pago.folio = respuesta["folio"]
    pag_pago.resultado_tiempo = datetime.now(tz=LOCAL_HUSO_HORARIO)
    pag_pago.resultado_xml = respuesta_xml
    db.add(pag_pago)
    db.commit()
    # db.refresh(pag_pago)

    # Entregar
    return PagResultadoOut(
        id_hasheado=cifrar_id(pag_pago.id),
        autoridad_clave=pag_pago.autoridad.clave,
        autoridad_descripcion=pag_pago.autoridad.descripcion,
        autoridad_descripcion_corta=pag_pago.autoridad.descripcion_corta,
        cantidad=pag_pago.cantidad,
        nombres=pag_pago.cit_cliente.nombres,
        apellido_primero=pag_pago.cit_cliente.apellido_primero,
        apellido_segundo=pag_pago.cit_cliente.apellido_segundo,
        email=pag_pago.email,
        estado=pag_pago.estado,
        folio=pag_pago.folio,
        resultado_tiempo=pag_pago.resultado_tiempo,
        total=pag_pago.total,
    )
