from django.db import models


class UpdatedMixin:
    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    class Meta:
        abstract = True
