import uuid
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from app.public.mixins import BaseEmailMixin
from authentication.models import User
from .serializers import UserCreateSerializer
from django.conf import settings


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
