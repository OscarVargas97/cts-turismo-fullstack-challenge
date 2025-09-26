from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from authentication.models import User
from phonenumber_field.serializerfields import PhoneNumberField
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "is_active"]
        read_only_fields = ["is_active"]

    def update(self, instance, validated_data):
        instance.is_active = True
        instance.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=True)  # Validación automática

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone_number",
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["password"]

    def create(self, validated_data):
        user = self.context["user"]
        user.set_password(validated_data["password"])
        user.save()
        return user
