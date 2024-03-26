import uuid

from django.db import models


class BaseUUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        max_length=255,
        auto_created=True,
        editable=False,
        default=uuid.uuid4,
    )

    class Meta:
        abstract = True


class BaseCreatedUpdatedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
