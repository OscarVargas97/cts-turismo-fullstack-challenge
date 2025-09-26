from rest_framework.exceptions import ValidationError, NotFound


class TokenExpiredException(ValidationError):
    def __init__(self, email):
        detail = {"error": "Token expired", "email": email}
        super().__init__(detail)


class InvalidTokenException(ValidationError):
    def __init__(self):
        super().__init__({"error": "Invalid token"})


class InvalidTokenPurposeException(ValidationError):
    def __init__(self):
        super().__init__({"error": "Invalid token purpose"})


class TokenNotFoundException(NotFound):
    def __init__(self):
        super().__init__({"error": "Token not found"})


class TokenEncryptionException(ValidationError):
    def __init__(self):
        super().__init__({"error": "Invalid token encryption"})


class TokenAlreadyUsedException(ValidationError):
    def __init__(self):
        super().__init__({"error": "Token already used"})
