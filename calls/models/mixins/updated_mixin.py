from django.db import models


class UpdatedMixin:
    created = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
