import uuid
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework.views import APIView
from app.public.mixins import BaseEmailMixin
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed, NotFound
from authentication.models import User
from django.utils.encoding import force_bytes


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
