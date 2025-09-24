import uuid
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from app.public.mixins import BaseEmailMixin
from authentication.models import User
from .serializers import UserCreateSerializer, UserSerializer
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(CreateAPIView, BaseEmailMixin):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    model = User

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(
            {"message": "Usuario creado correctamente."}, status=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)
        self._handle_email(request)
        return result

    def perform_create(self, serializer):
        super().perform_create(serializer)
        user = serializer.instance
        payload_raw = f"{str(user.uuid)}:::{default_token_generator.make_token(user)}"
        payload = urlsafe_base64_encode(force_bytes(payload_raw))

        verification_link = f"{settings.FRONTEND_URL}/verify-email/{payload}"
        self.destination_email = [user.email]
        self.email_subject = "Verificación de correo electrónico"
        self.email_message = f"Por favor, verifique su correo electrónico haciendo clic en el siguiente enlace: {verification_link}"


class MailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        full_token = urlsafe_base64_decode(request.data.get("token")).decode("utf-8")
        print("entramos")
        if not full_token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            uuid_str, token = full_token.split(":::")
            user_uuid = uuid.UUID(uuid_str)
            user = User.objects.get(uuid=user_uuid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            print(full_token)
            print("Error al procesar token:", repr(e))
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            pwd_reset_raw = f"pwd_reset:::{str(user.uuid)}:::{default_token_generator.make_token(user)}"
            pwd_reset_token = urlsafe_base64_encode(force_bytes(pwd_reset_raw))

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "password_reset_token": pwd_reset_token,
                }
            )
        else:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class SendMailVerificationView(APIView, BaseEmailMixin):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        uuid = request.data.get("uuid")
        if not uuid:
            raise AuthenticationFailed("Email is required")
        self.user = User.objects.filter(uuid=uuid).first()
        if self.user.is_active:
            raise AuthenticationFailed("User is already active")
        payload = urlsafe_base64_encode(
            f"{self.user.uuid.bytes}:::{default_token_generator.make_token(self.user)}"
        )
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{payload}/"
        self.destination_email = [self.user.email]
        self.email_subject = "Verificación de correo electrónico"
        self.email_message = f"Por favor, verifique su correo electrónico haciendo clic en el siguiente enlace: {verification_link}"
        self._handle_email(request)
        return Response({"message": "Email sent"})
