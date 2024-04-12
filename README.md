# pjecz-citas-v2-cliente-api-oauth2

API del Sistema de Citas hecho con FastAPI.

## Mejores prácticas

En la versión 3 usa las recomendaciones de [I've been abusing HTTP Status Codes in my APIs for years](https://blog.slimjim.xyz/posts/stop-using-http-codes/) que recomienda entregar un _status code_ **200** y un _body_ con el atributo `success` que indique si la operación fue exitosa o no, asi como un `message` donde explique el error.

### Respuesta exitosa

Status code: **200**

Body que entrega un listado

    {
        "success": true,
        "message": "Success",
        "result": {
            "total": 2812,
            "items": [ { "id": 1, ... } ],
            "limit": 100,
            "offset": 0
        }
    }

Body que entrega un item

    {
        "success": true,
        "message": "Success",
        "id": 123,
        ...
    }

### Respuesta fallida: registro no encontrado

Status code: **200**

Body

    {
        "success": false,
        "message": "No employee found for ID 100"
    }
