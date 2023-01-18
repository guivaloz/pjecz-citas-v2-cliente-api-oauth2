"""
Web Pay Plus
"""
import os
import asyncio

from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import requests

from lib.AESEncryption import AES128Encryption

load_dotenv()  # Take environment variables from .env

RESPUESTA_EXITO = "approved"
RESPUESTA_DENEGADA = "denied"
RESPUESTA_ERROR = "error"


def _create_chain_xml(pago_id, amount, email, description, cit_client_id):
    """Crear cadena XML"""
    root = ET.Element("P")

    business = ET.SubElement(root, "business")
    ET.SubElement(business, "id_company").text = "SNBX"  # TODO: Nombre asignado a nuestra organización. Cambiarla al recibirla por parte del Banco
    ET.SubElement(business, "id_branch").text = "01SNBXBRNCH"  # TODO: ID asignado a nuestra organización, Cambiarla al recibirla por parte del Banco
    ET.SubElement(business, "user").text = os.getenv("WPP_USER")
    ET.SubElement(business, "pwd").text = os.getenv("WPP_PASS")

    ET.SubElement(root, "version").text = "IntegraWPP"

    url = ET.SubElement(root, "url")
    ET.SubElement(url, "reference").text = str(pago_id)
    ET.SubElement(url, "amount").text = str(amount)
    ET.SubElement(url, "moneda").text = "MXN"
    ET.SubElement(url, "canal").text = "W"
    ET.SubElement(url, "omitir_notif_default").text = "0"
    ET.SubElement(url, "st_correo").text = "1"
    ET.SubElement(url, "mail_cliente").text = email

    data = ET.SubElement(url, "datos_adicionales")
    # Descripción del Servicio
    data1 = ET.SubElement(data, "data")
    data1.attrib["id"] = "1"
    data1.attrib["display"] = "true"
    label1 = ET.SubElement(data1, "label")
    label1.text = "Servicio"
    value1 = ET.SubElement(data1, "value")
    value1.text = description
    # Descripción del Cliente
    data2 = ET.SubElement(data, "data")
    data2.attrib["id"] = "2"
    data2.attrib["display"] = "false"
    label2 = ET.SubElement(data2, "label")
    label2.text = "Cliente ID"
    value2 = ET.SubElement(data2, "value")
    value2.text = str(cit_client_id)

    return ET.tostring(root, encoding="unicode")


def _encrypt_chain(chain: str):
    """Cifrar cadena XML"""
    key = os.getenv("WPP_KEY")
    if key is None:
        return None
    aes_encryptor = AES128Encryption()
    ciphertext = aes_encryptor.encrypt(chain, key)
    return ciphertext


def _decrypt_chain(chain_encrypted: str):
    """Descifrar cadena XML"""
    key = os.getenv("WPP_KEY")
    if key is None:
        raise Exception("Falta declarar la variable de entorno WPP_KEY.")
    aes_encryptor = AES128Encryption()
    plaintext = aes_encryptor.decrypt(key, chain_encrypted)
    return plaintext


async def _send_chain(chain: str):
    """Send to WPP"""

    # Get the commerce ID
    commerce_id = os.getenv("WPP_COMMERCE_ID")
    if commerce_id is None:
        raise ValueError("No se ha definido el WPP_COMMERCE_ID")

    # Get the WPP URL
    wpp_url = os.getenv("WPP_URL")
    if wpp_url is None:
        raise ValueError("No se ha definido el WPP_URL")

    # Pack the chain
    root = ET.Element("pgs")
    ET.SubElement(root, "data0").text = commerce_id
    ET.SubElement(root, "data").text = chain

    chain_bytes = ET.tostring(root, encoding="unicode")

    # Se prepara el envío del xml vía POST a la url de WPP
    payload = "xml=" + chain_bytes
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", wpp_url, headers=headers, data=payload)

    # Return
    return response.text


def _get_url_from_xml_encrypt(xml_encrypt: str):
    """Extrae la url del xml de respuesta"""
    xml = _decrypt_chain(xml_encrypt)
    root = ET.fromstring(xml)
    return root.find("nb_url").text


def create_pay_link(pago_id: int, email: str, service_detail: str, cit_client_id: int, amount: float):
    """Regresa el link para mostrar el formulario de pago"""

    chain = _create_chain_xml(
        pago_id=pago_id,
        amount=amount,
        email=email,
        description=service_detail,
        cit_client_id=cit_client_id,
    )
    chain_encrypt = _encrypt_chain(chain).decode()  # bytes
    respuesta = None

    try:
        respuesta = asyncio.run(_send_chain(chain_encrypt))
    except asyncio.TimeoutError as error:
        raise Exception(f"No hay respuesta en el limite de tiempo. {str(error)}")
    except Exception as error:
        raise Exception(f"Algo a salido mal en el envío. {str(error)}")

    # Respuesta recibida por el Banco, hay que descifrarla
    if respuesta != "" or respuesta is not None:
        url_pay = _get_url_from_xml_encrypt(respuesta)
        return url_pay  # URL del link de formulario de pago

    return None


def get_response(xml_encrypt_str: str):
    """Entrega una respuesta procesada"""
    respuesta = {
        "pago_id": None,
        "respuesta": None,
        "folio": None,
        "auth": None,
        "email": None,
    }

    # procesar el xml encriptado
    xml = _decrypt_chain(xml_encrypt_str)
    xml = _clean_xml(xml)
    root = ET.fromstring(xml)

    # Obtener nodos de respuesta
    respuesta["pago_id"] = root.find("reference").text
    respuesta["respuesta"] = root.find("response").text
    respuesta["folio"] = root.find("foliocpagos").text
    respuesta["auth"] = root.find("auth").text
    respuesta["email"] = root.find("email").text

    return respuesta


def _clean_xml(xml_str: str):
    """Quita los comentarios del archivo XML que no puede procesar la clase XML"""
    xml_limpio = ""
    for line in xml_str.split("\n"):
        if "<?" not in line:
            xml_limpio += line

    return xml_limpio
