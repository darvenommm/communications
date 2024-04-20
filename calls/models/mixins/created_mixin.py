from django.db import models


class CreatedMixin:
    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        abstract = True
