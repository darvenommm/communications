"""Module with UpdatedMixin."""

from django.db import models


class UpdatedMixin:
    """Mixin that adds update_at field."""

    updated_at = models.DateTimeField(auto_now=True, blank=True, editable=False)

    class Meta:
        """Class Meta."""

        abstract = True
