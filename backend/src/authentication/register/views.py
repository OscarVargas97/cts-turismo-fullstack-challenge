import uuid
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from emails.mixins import TemplateEmailMixin
from authentication.models import User
from ..serializers import UserCreateSerializer, UserSerializer
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from ..token_manager import TokenManager
from app.public.mixins import ResponseMixin
from raffles.models import (
    Participant,
    Raffle,
    RaffleStatus,
)
from raffles.serializer import (
    RaffleSerializer,
)


class RegisterView(ResponseMixin, CreateAPIView, TemplateEmailMixin):
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    model = User

    template_key = "verification_email"

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return self.success_response(
            message="Usuario creado correctamente", status_code=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        result = super().create(request, *args, **kwargs)

        self._handle_email(request)
        return result

    def perform_create(self, serializer):
        super().perform_create(serializer)
        user = serializer.instance

        token_manager = TokenManager()
        token = token_manager.create_token(user, purpose="email_verification")

        verification_link = f"{settings.FRONTEND_URL}/auth/verify/{token}"
        self.from_email = settings.EMAIL_HOST_USER
        self.destination_email = [user.email]
        self.template_context = {
            "username": user.username,
            "verification_link": verification_link,
            "company_name": "Mi Empresa",
        }


class MailVerificationView(ResponseMixin, APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST
            )

        token_manager = TokenManager()
        payload_or_error = token_manager.validate_token(
            token, purpose="email_verification"
        )

        try:
            user = User.objects.get(uuid=payload_or_error.get("uuid"))
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=["is_active"])

        pwd_reset_token = token_manager.create_token(user, purpose="password_reset")

        raffle_join_result = None
        try:
            active_raffle = Raffle.objects.get(status=RaffleStatus.ACTIVE)

            if not Participant.objects.filter(user=user, raffle=active_raffle).exists():
                if active_raffle.max_participants:
                    current_participants = Participant.objects.filter(
                        raffle=active_raffle
                    ).count()
                    if current_participants >= active_raffle.max_participants:
                        raffle_join_result = {
                            "error": "El sorteo ha alcanzado el límite de participantes"
                        }
                    else:
                        Participant.objects.create(user=user, raffle=active_raffle)
                        raffle_join_result = {
                            "message": "Te has registrado exitosamente en el sorteo",
                            "raffle": RaffleSerializer(active_raffle).data,
                        }
                else:
                    Participant.objects.create(user=user, raffle=active_raffle)
                    raffle_join_result = {
                        "message": "Te has registrado exitosamente en el sorteo",
                        "raffle": RaffleSerializer(active_raffle).data,
                    }
            else:
                raffle_join_result = {"error": "Ya estás participando en este sorteo"}

        except Raffle.DoesNotExist:
            raffle_join_result = {"error": "No hay sorteos activos en este momento"}

        # Respuesta final
        return self.success_response(
            message="Correo verificado correctamente",
            data={
                "user": UserSerializer(user).data,
                "password_reset_token": pwd_reset_token,
            },
        )


class SendMailVerificationView(ResponseMixin, APIView, TemplateEmailMixin):
    permission_classes = ()
    authentication_classes = ()
    template_key = "verification_email"

    def post(self, request):
        email = request.data.get("email")
        if not uuid:
            raise AuthenticationFailed("Email is required")
        self.user = User.objects.filter(email=email).first()
        if not self.user:
            raise AuthenticationFailed("User not found")
        if self.user.is_active:
            raise AuthenticationFailed("User is already active")

        token_manager = TokenManager()
        token = token_manager.create_token(self.user, purpose="email_verification")

        verification_link = f"{settings.FRONTEND_URL}/auth/verify/{token}"
        self.destination_email = [self.user.email]
        self.from_email = settings.EMAIL_HOST_USER
        self.destination_email = [self.user.email]
        self.template_context = {
            "username": self.user.username,
            "verification_link": verification_link,
            "company_name": "Mi Empresa",
        }
        self._handle_email(request)

        return self.success_response(message="Se ha enviado el correo")
