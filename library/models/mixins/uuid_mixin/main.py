"""Module with Uuid Mixin."""

from uuid import uuid4

from django.db import models


class UuidMixin(models.Model):
    """Mixin that adds id uuid field."""

    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        """Class meta."""

        abstract = True
