from .serializers import EmailSerializer
from .types import EmailData
from .tasks import send_email_task
from .templates import EMAIL_TEMPLATES
from typing import Optional


class BaseEmailMixin:
    from_email: Optional[str] = None
    email_subject: str = ""
    destination_email: list[str] = []

    def _get_recipient_list(self) -> list[str]:
        if isinstance(self.destination_email, str):
            return [self.destination_email]
        elif isinstance(self.destination_email, list):
            return self.destination_email
        return []

    def _get_properties_mail_data(
        self, message: str, html_message: Optional[str] = None
    ) -> EmailData:
        return EmailData(
            subject=self.email_subject,
            message=message,
            from_email=self.from_email or "default@example.com",
            recipient_list=self._get_recipient_list(),
            html_message=html_message,
        )

    def _handle_email(self, message: str, html_message: Optional[str] = "") -> None:
        email_data = self._get_properties_mail_data(message, html_message)
        serializer: EmailSerializer = EmailSerializer(data=email_data)
        serializer.is_valid(raise_exception=True)
        send_email_task.delay(**serializer.validated_data)


class CustomEmailMixin(BaseEmailMixin):
    email_message: str = ""

    def _handle_email(self, request, html_message: Optional[str] = None) -> None:
        if not self.email_message:
            raise ValueError("email_message no puede estar vacío")
        super()._handle_email(self.email_message, html_message=html_message)


class TemplateEmailMixin(CustomEmailMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.template_context is None:
            self.template_context = {}

    def _validate_template_key(self):
        if not self.template_key:
            raise ValueError(
                "template_key debe estar definido para usar TemplateEmailMixin"
            )
        if self.template_key not in EMAIL_TEMPLATES:
            raise ValueError(f"No existe el template con clave '{self.template_key}'")

    def _render_template_message(self) -> str:
        self._validate_template_key()

        template_data = EMAIL_TEMPLATES[self.template_key]
        subject = template_data.get("subject", "Sin subject definido")
        html_body = template_data.get("html_body", "")

        self.email_subject = subject

        context_with_subject = {"subject": subject, **self.template_context}
        try:
            return html_body.format(**context_with_subject)
        except KeyError as e:
            raise ValueError(f"Falta una variable en el contexto: {e}")

    def _handle_email(self, request, html_message: Optional[str] = None) -> None:
        html_message = self._render_template_message()
        self.email_message = html_message  # texto plano
        super()._handle_email(request, html_message=html_message)
