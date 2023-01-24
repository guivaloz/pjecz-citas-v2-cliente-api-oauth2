"""
WPP Obtener al URL del Banco para el Formulario de Pago

"""
import argparse
import asyncio

from lib.santander_web_pay_plus import create_chain_xml, encrypt_chain, create_chain_xml_sender, send_chain, decrypt_chain, get_url_from_xml_encrypt, create_pay_link

from lib.exceptions import (
    CitasTimeoutError,
    CitasUnknownError,
    CitasNotValidAnswerError,
    CitasDesencryptError,
    CitasGetURLFromXMLEncryptedError,
)


def main():
    """Main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("nivel", type=str, choices=["xml", "xml_encriptado", "xml_de_envio", "respuesta_banco", "respuesta_banco_xml", "respuesta_banco_url", "completo"], default="completo", help="Tipo de respuesta")

    args = parser.parse_args()

    # Crear cadena XML
    chain = create_chain_xml(
        pago_id=100,
        amount=250.55,
        email="prueba@pjecz.gob.mx",
        description="Servicio de Prueba",
        cit_client_id=1007,
    )

    if args.nivel == "completo":
        print("===[ Proceso completo payload para obtener url del banco ]===")
        url = create_pay_link(pago_id=100, amount=250.55, email="prueba@pjecz.gob.mx", service_detail="Servicio de Prueba", cit_client_id=1007)
        print(url)
        return 0

    if args.nivel == "xml":
        print("===[ XML generado para enviar al Banco ]===")
        print(chain)
        return 0

    chain_encrypt = encrypt_chain(chain).decode()  # bytes

    if args.nivel == "xml_encriptado":
        print("===[ Cadena de texto que representa el XML encriptado listo para enviar al Banco ]===")
        print(chain_encrypt)
        return 0

    xml_sender = create_chain_xml_sender(chain_encrypt)

    if args.nivel == "xml_de_envio":
        print("===[ XML que se envía al Banco para la obtención del URL de formulario ]===")
        print(xml_sender)
        return 0

    # Enviar cadena XML a WPP
    respuesta = None
    try:
        respuesta = asyncio.run(send_chain(chain_encrypt))
    except asyncio.TimeoutError as error:
        raise CitasTimeoutError("Error porque se agoto el tiempo de espera con WPP") from error
    except Exception as error:
        raise CitasUnknownError("Error al tratar de enviar la cadena XML a WPP") from error

    # Si no hay respuesta, causar error
    if respuesta is None or respuesta == "" or respuesta == "\n":
        raise CitasNotValidAnswerError("Error en la respuesta de WPP (respuesta vacía)")

    if args.nivel == "respuesta_banco":
        print("===[ Respuesta del Banco: Cadena de texto que representa un XML encriptado ]===")
        print(respuesta)
        return 0

    # Se desencripta el XML enviado por el Banco
    try:
        xml = decrypt_chain(respuesta)
    except Exception as error:
        raise CitasDesencryptError("No se puede desencriptar el XML del Banco") from error

    if args.nivel == "respuesta_banco_xml":
        print("===[ XML enviado por el Banco como respuesta ]===")
        print(xml)
        return 0

    # Descifrar la respuesta y extraer la url
    try:
        url = get_url_from_xml_encrypt(respuesta)
    except Exception as error:
        raise CitasGetURLFromXMLEncryptedError("Error al obtener la URL del Banco desde su XML encriptado") from error

    if args.nivel == "url_banco":
        print("===[ URL del Formulario del Banco ]===")
        print(url)
        return 0


if __name__ == "__main__":
    main()
