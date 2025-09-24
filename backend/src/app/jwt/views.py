from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from app.public.handlers import CookieHandler
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        self.user = serializer.user
        return self.build_response(request, serializer.validated_data)

    def build_response(self, request, serializer: dict) -> Response:
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CookieTokenObtainPairView(CustomTokenObtainPairView):

    def build_response(self, request, tokens: dict) -> Response:
        response = Response({"access": tokens["access"]}, status=status.HTTP_200_OK)
        CookieHandler.set_jwt_cookies(response, "refresh", tokens["refresh"])
        return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh")
        print(request.COOKIES.get("refresh"))
        if not refresh_token:
            return Response({"detail": "No refresh token provided"}, status=401)

        request.data["refresh"] = refresh_token
        try:
            response = super().post(request, *args, **kwargs)

            if "refresh" in response.data:
                CookieHandler.set_jwt_cookies(
                    response, "refresh", response.data["refresh"]
                )
                del response.data["refresh"]

            return response

        except TokenError:
            return Response({"detail": "Invalid refresh token"}, status=401)
