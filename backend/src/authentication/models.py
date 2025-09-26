from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

from django.db import models
from django.utils import timezone

from app.public.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=False)  # Valor por defecto cambiado
    phone_number = PhoneNumberField(blank=True, null=True, region=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "uuid"], name="unique_username_uuid"
            )
        ]


class UserToken(BaseModel):
    PURPOSE_CHOICES = [
        ("email_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
        ("two_factor", "Two Factor Authentication"),
        ("custom", "Custom Purpose"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("used", "Used"),
        ("expired", "Expired"),
        ("invalidated", "Invalidated"),
    ]

    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tokens")
    token = models.CharField(max_length=512, unique=True)
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    expires_at = models.DateTimeField(null=True, blank=True)
    used_at = models.DateTimeField(null=True, blank=True)
    invalidated_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["token"]),
            models.Index(fields=["status"]),
            models.Index(fields=["purpose"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.purpose} - {self.status}"

    def mark_as_used(self):
        self.status = "used"
        self.used_at = timezone.now()
        self.save()

    def mark_as_invalidated(self):
        self.status = "invalidated"
        self.invalidated_at = timezone.now()
        self.save()

    def mark_as_expired(self):
        self.status = "expired"
        self.save()

    def is_valid(self):
        if self.status != "active":
            return False

        if self.expires_at and timezone.now() > self.expires_at:
            self.mark_as_expired()
            return False

        latest_token = (
            UserToken.objects.filter(user=self.user, purpose=self.purpose)
            .order_by("-id")
            .first()
        )
        if latest_token.id != self.id:
            return False

        return True
