from django.contrib.auth.models import AbstractUser
from django.db import models


from app.public.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["username", "uuid"], name="unique_username_uuid"
            )
        ]
