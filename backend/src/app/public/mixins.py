from rest_framework import status
from app.jwt.responses import custom_response


class ResponseMixin:
    def success_response(
        self, message="Operación exitosa", data=None, status_code=status.HTTP_200_OK
    ):
        return custom_response(
            success=True, status_code=status_code, message=message, data=data
        )

    def error_response(
        self,
        message="Ocurrió un error",
        errors=None,
        status_code=status.HTTP_400_BAD_REQUEST,
    ):
        return custom_response(
            success=False, status_code=status_code, message=message, errors=errors
        )
