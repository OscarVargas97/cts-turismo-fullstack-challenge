import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from cryptography.fernet import Fernet
from .models import UserToken
import base64
from .exceptions import (
    TokenExpiredException,
    InvalidTokenException,
    InvalidTokenPurposeException,
    TokenNotFoundException,
    TokenEncryptionException,
    TokenAlreadyUsedException,
)


class TokenManager:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = getattr(settings, "TOKEN_JWT_ALGORITHM", "HS256")

    def create_token(self, user, purpose, expires_in=300, metadata=None):
        if not self._can_create_token(user, purpose):
            raise ValueError(f"Cannot create token for purpose: {purpose}")

        payload = {
            "uuid": str(user.uuid),
            "email": user.email,
            "purpose": purpose,
            "exp": datetime.utcnow() + timedelta(seconds=expires_in),
        }

        jwt_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        compact_token = (
            base64.urlsafe_b64encode(jwt_token.encode()).rstrip(b"=").decode()
        )

        expires_at = timezone.now() + timedelta(seconds=expires_in)

        UserToken.objects.create(
            user=user,
            token=compact_token,
            purpose=purpose,
            expires_at=expires_at,
            metadata=metadata or {},
        )

        return compact_token

    def validate_token(self, compact_token, purpose):
        try:
            token_record = UserToken.objects.get(token=compact_token, purpose=purpose)
        except UserToken.DoesNotExist:
            raise TokenNotFoundException()

        if token_record.status == "used":
            raise TokenAlreadyUsedException()

        try:
            jwt_token = self._decode_compact_token(compact_token)
        except Exception:
            raise TokenEncryptionException()

        try:
            payload = jwt.decode(
                jwt_token, self.secret_key, algorithms=[self.algorithm]
            )
        except jwt.ExpiredSignatureError:
            email = self._get_email_from_token(compact_token)
            token_record.mark_as_used()
            raise TokenExpiredException(email)
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

        if payload.get("purpose") != purpose:
            raise InvalidTokenPurposeException()

        token_record.mark_as_used()
        return payload

    def decode_token(self, compact_token):
        try:
            jwt_token = self._decode_compact_token(compact_token)
            return jwt.decode(jwt_token, self.secret_key, algorithms=[self.algorithm])
        except Exception:
            return None

    def _decode_compact_token(self, compact_token: str) -> str:
        padded_token = compact_token + "=" * (-len(compact_token) % 4)
        return base64.urlsafe_b64decode(padded_token.encode()).decode()

    def _can_create_token(self, user, purpose):
        if purpose == "email_verification":
            return not user.is_active
        elif purpose == "password_reset":
            return True
        return False

    def _get_email_from_token(self, compact_token):
        token = self._decode_compact_token(compact_token)
        payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            options={"verify_exp": False},
        )
        if not payload:
            return None
        email = payload.get("email")
        return email
