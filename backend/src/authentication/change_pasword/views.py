import uuid
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.views import APIView
from app.public.mixins import BaseEmailMixin
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from authentication.models import User
from django.utils.encoding import force_bytes
from .serializers import ChangePasswordSerializer
from rest_framework.permissions import AllowAny


class ChangePasswordRequestView(APIView, BaseEmailMixin):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        email = request.data.get("email")
        if not email:
            raise AuthenticationFailed("Email is required")
        user = User.objects.filter(email__iexact=email.strip()).first()

        if user is None:
            raise NotFound("User not found")
        payload_raw = (
            f"pwd_reset:::{str(user.uuid)}:::{default_token_generator.make_token(user)}"
        )
        payload = urlsafe_base64_encode(force_bytes(payload_raw))
        verification_link = f"{settings.FRONTEND_URL}/reset-password/{payload}"
        self.destination_email = [user.email]
        self.email_subject = "Cambio de contraseña"
        self.email_message = f"Para cambiar su contraseña, haga clic en el siguiente enlace: {verification_link}"
        self._handle_email(request)
        return Response({"message": "Email sent"})


class ChangePasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = request.data.get("token")
            full_token = urlsafe_base64_decode(token).decode("utf-8")
            prefix, uuid_str, token = full_token.split(":::")

            if prefix != "pwd_reset":
                raise ValidationError("Token inválido")

            user = User.objects.get(uuid=uuid.UUID(uuid_str))

            if not default_token_generator.check_token(user, token):
                raise ValidationError("Token expirado o inválido")

            user.set_password(serializer.validated_data["new_password"])
            user.save()

            return Response({"message": "Contraseña actualizada exitosamente"})

        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            raise ValidationError("Token inválido")
        except Exception as e:
            raise ValidationError(str(e))
