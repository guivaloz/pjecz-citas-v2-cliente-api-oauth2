"""
Prueba de PPA Solicitud
"""
import requests

# API_PPA_SOLICITUD_URL = "http://127.0.0.1:8005/v3/ppa_solicitudes"
API_PPA_SOLICITUD_URL = "http://justicia:7086/v3/ppa_solicitudes"
API_TIMEOUT = 12

BANCO_FOTOGRAFIAS_RUTA = "/home/guivaloz/Pictures/PJECZ Tres de Tres"
IDENTIFICACION_OFICIAL_ARCHIVO = "ine.pdf"
COMPROBANTE_DOMICILIO_ARCHIVO = "cfe.pdf"
AUTORIZACION_ARCHIVO = "carta.pdf"


def test_ppa_solicitud():
    """
    Prueba de PPA Solicitud
    """

    # Datos de prueba
    datos = {
        "autoridad_clave": "TRC-J1-CIV",
        "cit_cliente_curp": "VALG710406HNLLZL04",
        "cit_cliente_email": "guillermo.valdes@pjecz.gob.mx",
        "cit_cliente_nombres": "Guillermo",
        "cit_cliente_apellido_primero": "Valdes",
        "cit_cliente_apellido_segundo": "Lozano",
        "cit_cliente_telefono": "8711542682",
        "domicilio_calle": "Juana de Arco",
        "domicilio_numero": "213",
        "domicilio_colonia": "Roma",
        "domicilio_cp": 24000,
        "compania_telefonica": "ATT",
        "numero_expediente": "1/2022",
    }

    # Enviar los datos
    try:
        respuesta = requests.post(
            f"{API_PPA_SOLICITUD_URL}/solicitar",
            json=datos,
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        assert False, "No se pudo conectar con la API. " + str(error)
    except requests.exceptions.Timeout as error:
        assert False, "Tiempo de espera agotado al conectar con la API. " + str(error)
    except requests.exceptions.HTTPError as error:
        assert False, "Error HTTP la API arrojó un problema: " + str(error)
    except requests.exceptions.RequestException as error:
        assert False, "Error desconocido con la API . " + str(error)
    resultado = respuesta.json()

    # Verificar que el resultado sea exitoso
    if not "success" in resultado:
        assert False, "La respuesta no tiene el campo success"
    if not resultado["success"]:
        if "message" in resultado:
            assert False, resultado["message"]
        assert False, "La respuesta dice que la operacion fallo"

    # Obtenemos el id_hasheado que se usará para subir los archivos
    id_hasheado = resultado["id_hasheado"]

    # Archivo con la identificación oficial
    try:
        identificacion_oficial = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{IDENTIFICACION_OFICIAL_ARCHIVO}", "rb")
    except FileNotFoundError as error:
        assert False, "No se pudo abrir el archivo de identificación oficial. " + str(error)

    # Enviar la identificación oficial
    try:
        respuesta = requests.post(
            f"{API_PPA_SOLICITUD_URL}/subir/identificacion_oficial",
            params={"id_hasheado": id_hasheado},
            files={"archivo": identificacion_oficial},
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        assert False, "No se pudo conectar con la API. " + str(error)
    except requests.exceptions.Timeout as error:
        assert False, "Tiempo de espera agotado al conectar con la API. " + str(error)
    except requests.exceptions.HTTPError as error:
        assert False, "Error HTTP la API arrojó un problema: " + str(error)
    except requests.exceptions.RequestException as error:
        assert False, "Error desconocido con la API . " + str(error)
    resultado = respuesta.json()

    # Verificar que el resultado sea exitoso
    if not "success" in resultado:
        assert False, "La respuesta no tiene el campo success"
    if not resultado["success"]:
        if "message" in resultado:
            assert False, resultado["message"]
        assert False, "La respuesta dice que la operacion fallo"

    # Cerrar archivo
    identificacion_oficial.close()

    # Archivo con el comprobante de domicilio
    try:
        comprobante_domicilio = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{COMPROBANTE_DOMICILIO_ARCHIVO}", "rb")
    except FileNotFoundError as error:
        assert False, "No se pudo abrir el archivo de comprobante de domicilio. " + str(error)

    # Enviar el comprobante de domicilio
    try:
        respuesta = requests.post(
            f"{API_PPA_SOLICITUD_URL}/subir/comprobante_domicilio",
            params={"id_hasheado": id_hasheado},
            files={"archivo": comprobante_domicilio},
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        assert False, "No se pudo conectar con la API. " + str(error)
    except requests.exceptions.Timeout as error:
        assert False, "Tiempo de espera agotado al conectar con la API. " + str(error)
    except requests.exceptions.HTTPError as error:
        assert False, "Error HTTP la API arrojó un problema: " + str(error)
    except requests.exceptions.RequestException as error:
        assert False, "Error desconocido con la API . " + str(error)
    resultado = respuesta.json()

    # Verificar que el resultado sea exitoso
    if not "success" in resultado:
        assert False, "La respuesta no tiene el campo success"
    if not resultado["success"]:
        if "message" in resultado:
            assert False, resultado["message"]
        assert False, "La respuesta dice que la operacion fallo"

    # Cerrar archivo
    comprobante_domicilio.close()

    # Archivo con la autorización
    try:
        autorizacion = open(f"{BANCO_FOTOGRAFIAS_RUTA}/{AUTORIZACION_ARCHIVO}", "rb")
    except FileNotFoundError as error:
        assert False, "No se pudo abrir el archivo de autorización. " + str(error)

    # Enviar el comprobante de domicilio
    try:
        respuesta = requests.post(
            f"{API_PPA_SOLICITUD_URL}/subir/autorizacion",
            params={"id_hasheado": id_hasheado},
            files={"archivo": autorizacion},
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        assert False, "No se pudo conectar con la API. " + str(error)
    except requests.exceptions.Timeout as error:
        assert False, "Tiempo de espera agotado al conectar con la API. " + str(error)
    except requests.exceptions.HTTPError as error:
        assert False, "Error HTTP la API arrojó un problema: " + str(error)
    except requests.exceptions.RequestException as error:
        assert False, "Error desconocido con la API . " + str(error)
    resultado = respuesta.json()

    # Verificar que el resultado sea exitoso
    if not "success" in resultado:
        assert False, "La respuesta no tiene el campo success"
    if not resultado["success"]:
        if "message" in resultado:
            assert False, resultado["message"]
        assert False, "La respuesta dice que la operacion fallo"

    # Cerrar archivo
    autorizacion.close()

    # Mostrar los resultado de la respuesta
    print(resultado)

    # La prueba fue exitosa
    assert True


if __name__ == "__main__":
    test_ppa_solicitud()
