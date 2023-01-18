"""
WPP Creación de XML de respuesta del Banco (Santander)

"""
import argparse
import string
import random

from lib.pagos_banco import _encrypt_chain, RESPUESTA_EXITO, RESPUESTA_ERROR, RESPUESTA_DENEGADA

LEN_STR = 7


def main():
    """Main function"""

    parser = argparse.ArgumentParser()
    parser.add_argument("pago_id", type=int, help="El ID del pago")
    parser.add_argument("respuesta", type=str, choices=[RESPUESTA_EXITO, RESPUESTA_ERROR, RESPUESTA_DENEGADA], default=RESPUESTA_EXITO, help="Tipo de respuesta")

    args = parser.parse_args()

    # Datos a utilizar
    params = {
        "pago_id": int(args.pago_id),
        "respuesta": args.respuesta,
        "folio": "".join(random.choices(string.ascii_uppercase + string.digits, k=LEN_STR)),
        "auth": "".join(random.choices(string.ascii_uppercase + string.digits, k=LEN_STR)),
        "email": "cliente@correo.com",
        "amount": 400.00,
    }

    # Cargamos el Template de respuesta XML
    xml = ""
    with open("seed/respuesta_wpp.xml", "r") as file:
        for line in file:
            if "$" in line:
                indx_1 = line.find("$")
                indx_2 = line.rfind("$")
                var = line[indx_1 + 1 : indx_2]
                xml += line.replace("$" + var + "$", str(params[var]))
            else:
                xml += line

    # Encriptación del XML
    xml_encriptado = _encrypt_chain(xml).decode()

    # Impresión del resultado
    print("pago_id:", args.pago_id, "respuesta:", args.respuesta)
    print("XML de Respuesta del Banco (Santander) Encriptado")
    print(xml_encriptado)


if __name__ == "__main__":
    main()
