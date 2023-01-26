"""
WPP Desencripta el XML de respuesta del banco

"""
import argparse

from lib.santander_web_pay_plus import decrypt_chain, convert_xml_encrypt_to_dict
from lib.exceptions import CitasXMLReadError


def main():
    """Main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("xml_encriptado", type=str, help="Respuesta encriptada del Banco")

    args = parser.parse_args()

    xml = decrypt_chain(args.xml_encriptado)
    print("===[ XML desincriptado ]===")
    print(xml)

    try:
        resultado = convert_xml_encrypt_to_dict(args.xml_encriptado)
        print("===[ Lectura del XML ]===")
        print(resultado)
    except CitasXMLReadError as error:
        print(f"Error XML corrupto {error}.")
    except Exception as error:
        print(f"Error: {error}.")


if __name__ == "__main__":
    main()
