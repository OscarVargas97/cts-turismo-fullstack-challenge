from rest_framework import serializers

from .types import EmailData


class EmailSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    from_email = serializers.EmailField()
    recipient_list = serializers.ListField(child=serializers.EmailField())

    def save(self):
        return EmailData(**self.validated_data)

    def validate(self, data: dict) -> dict:
        return super().validate(data)
