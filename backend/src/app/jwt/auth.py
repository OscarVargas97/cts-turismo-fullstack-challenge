from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        cookie_name = settings.SIMPLE_JWT.get("AUTH_COOKIE", "access")
        token = request.COOKIES.get(cookie_name)

        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
        except AuthenticationFailed:
            return None

        try:
            user = self.get_user(validated_token)
            return user, validated_token
        except AuthenticationFailed:
            return None
