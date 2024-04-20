from django.db import models

from uuid import uuid4


class UuidMixin(models.Model):
    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True
