from django.db import models


class UpdatedMixin:
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
