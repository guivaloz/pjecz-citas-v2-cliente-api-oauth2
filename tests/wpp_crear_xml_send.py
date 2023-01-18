"""
WPP Creación de XML encriptados que pide el Banco Santander

"""
from lib.pagos_banco import _create_chain_xml, _encrypt_chain


def main():
    """Main function"""

    # Datos a utilizar
    pago_id = 98
    amount = 545.0
    email = "none@none.com"
    description = "CERTIFICACION DE MEDIADORES"
    cit_client_id = "16331"

    # Creación del XML con los datos asignados
    chain = _create_chain_xml(
        pago_id=pago_id,
        amount=amount,
        email=email,
        description=description,
        cit_client_id=cit_client_id,
    )
    # Encriptación del XML
    xml_encriptado = _encrypt_chain(chain).decode()

    # Impresión del resultado
    print("XML Encriptado")
    print(xml_encriptado)


if __name__ == "__main__":
    main()
