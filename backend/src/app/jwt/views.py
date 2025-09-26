from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

from .handlers import CookieHandler


class BaseTokenView:
    user = None
    tokens = None  # We'll store access and refresh here

    def build_response(self) -> Response:
        if not self.user:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user_data = {
            "uuid": str(self.user.uuid) if hasattr(self.user, "uuid") else None,
            "username": self.user.username,
            "email": self.user.email,
        }

        response = Response({"user": user_data}, status=status.HTTP_200_OK)

        # If tokens exist, set them in cookies
        if self.tokens:
            if "access" in self.tokens:
                CookieHandler.set_jwt_cookies(response, "access", self.tokens["access"])
            if "refresh" in self.tokens:
                CookieHandler.set_jwt_cookies(
                    response, "refresh", self.tokens["refresh"]
                )

        return response


class CustomTokenObtainPairView(BaseTokenView, TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        self.tokens = serializer.validated_data
        self.user = getattr(serializer, "user", None)

        return self.build_response()


class CustomTokenRefreshView(BaseTokenView, TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        self.tokens = serializer.validated_data
        access_token_str = serializer.validated_data.get("access")
        try:
            access_token = AccessToken(access_token_str)
            user_id = access_token.get("user_id")
        except Exception:
            user_id = None

        if user_id:
            try:
                self.user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                self.user = None
        else:
            self.user = None

        return self.build_response()
