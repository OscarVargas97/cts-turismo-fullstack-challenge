from rest_framework.response import Response
from django.conf import settings
from django.middleware.csrf import get_token


class CookieHandler:
    @staticmethod
    def get_cookie_options():
        if settings.DEBUG:
            return {
                "httponly": True,
                "secure": False,  # Desactivado en desarrollo
                "samesite": None,  # Permitir cualquier origen en desarrollo
                "max_age": 7 * 24 * 60 * 60,
            }
        else:
            return {
                "httponly": True,
                "secure": True,
                "samesite": "Lax",
                "max_age": 7 * 24 * 60 * 60,
            }

    @staticmethod
    def set_cookie(
        response: Response, key: str, value: str, options: dict = None
    ) -> None:
        default_options = CookieHandler.get_cookie_options()
        cookie_options = {**default_options, **(options or {})}
        response.set_cookie(key=key, value=value, **cookie_options)

    @staticmethod
    def set_jwt_cookies(response: Response, key: str, token: str) -> None:
        CookieHandler.set_cookie(response, key, token)
