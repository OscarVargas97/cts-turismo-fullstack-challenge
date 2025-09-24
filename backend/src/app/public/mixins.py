from typing import Any, Dict
from .tasks import send_email_task
from django.conf import settings

from .serializers import EmailSerializer
from .types import EmailData


class BaseEmailMixin:
    is_data_from_request: bool = False
    from_email: str = settings.EMAIL_HOST_USER
    destination_email = []
    email_subject: str = ""
    email_message: str = ""
    is_request_data: bool = False

    def _get_email_data(self, request) -> Dict[str, Any]:
        if self.is_data_from_request:
            return request.data
        return self._get_properties_mail_data()

    def _get_properties_mail_data(self) -> EmailData:
        recipient_list = (
            [self.destination_email]
            if isinstance(self.destination_email, str)
            else self.destination_email
        )
        return EmailData(
            subject=self.email_subject,
            message=self.email_message,
            from_email=self.from_email,
            recipient_list=recipient_list,
        )

    def _handle_email(self, request) -> None:
        get_mail_data = self._get_email_data(request)
        serializer: EmailSerializer = EmailSerializer(data=get_mail_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        send_email_task.delay(**data)
