"""
WPP Desencripta el XML de respuesta del banco

"""
import argparse

from lib.santander_web_pay_plus import decrypt_chain


def main():
    """Main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("xml_encriptado", type=str, help="Respuesta encriptada del Banco")

    args = parser.parse_args()

    respuesta = decrypt_chain(args.xml_encriptado)

    print("===[ XML desincriptado ]===")
    print(respuesta)


if __name__ == "__main__":
    main()
