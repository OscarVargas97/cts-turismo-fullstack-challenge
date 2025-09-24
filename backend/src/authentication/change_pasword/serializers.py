from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import re


class ChangePasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, min_length=8, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        required=True, min_length=8, write_only=True, style={"input_type": "password"}
    )

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise ValidationError({"confirm_password": "Las contraseñas no coinciden"})

        password = attrs["new_password"]

        if not re.search(r"[A-Z]", password):
            raise ValidationError("La contraseña debe contener al menos una mayúscula")

        if not re.search(r"[a-z]", password):
            raise ValidationError("La contraseña debe contener al menos una minúscula")

        if not re.search(r"\d", password):
            raise ValidationError("La contraseña debe contener al menos un número")
        return attrs
