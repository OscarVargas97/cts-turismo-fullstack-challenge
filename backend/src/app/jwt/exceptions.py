from rest_framework.views import exception_handler
from rest_framework import status
from .responses import custom_response  # importa tu función


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return custom_response(
            success=False,
            status_code=response.status_code,
            message="Error en la solicitud",
            errors=response.data,
        )
    else:
        # Error inesperado
        return custom_response(
            success=False,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error interno del servidor",
            errors=str(exc),
        )
