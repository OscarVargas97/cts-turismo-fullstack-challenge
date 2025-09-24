import uuid

from django.db import models
from django_softdelete.models import SoftDeleteModel


class BaseModel(SoftDeleteModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
