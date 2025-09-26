from rest_framework.response import Response
from rest_framework.views import APIView
from emails.mixins import TemplateEmailMixin
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, NotFound
from authentication.models import User
from ..serializers import ChangePasswordSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from ..token_manager import TokenManager
from app.public.mixins import ResponseMixin


class ChangePasswordRequestView(ResponseMixin, APIView, TemplateEmailMixin):
    permission_classes = ()
    authentication_classes = ()
    template_key = "change_password"  # clave correcta del template

    def post(self, request):
        email = request.data.get("email")
        if not email:
            raise AuthenticationFailed("Email is required")

        user = User.objects.filter(email__iexact=email.strip()).first()
        print("usuario", user)
        if not user:
            raise NotFound("User not found")

        token_manager = TokenManager()
        token = token_manager.create_token(user, purpose="password_reset")

        change_password_link = f"{settings.FRONTEND_URL}/auth/change-password/{token}"

        self.user = user
        self.from_email = settings.EMAIL_HOST_USER
        self.destination_email = [user.email]
        self.template_context = {
            "username": user.username,
            "change_password_link": change_password_link,
            "subject": "Cambio de contraseña",
            "company_name": "Mi Empresa",
        }

        self._handle_email(request)

        return self.success_response(
            message="Se ha enviado el correo para cambiar la contraseña"
        )


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = request.data.get("token")
        if not token:
            return Response(
                {"error": "Token requerido"}, status=status.HTTP_400_BAD_REQUEST
            )

        token_manager = TokenManager()
        payload_or_error = token_manager.validate_token(token, purpose="password_reset")

        try:
            user = User.objects.get(uuid=payload_or_error.get("uuid"))
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"message": "Contraseña actualizada exitosamente"})
