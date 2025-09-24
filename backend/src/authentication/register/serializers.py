from rest_framework import serializers
from authentication.models import User


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
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
        )
        return user
