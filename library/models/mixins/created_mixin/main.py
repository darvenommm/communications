"""Module with CreatedMixin."""

from django.db import models


class CreatedMixin:
    """Class that adds created_at field."""

    created_at = models.DateTimeField(auto_now_add=True, blank=True, editable=False)

    class Meta:
        """Class Meta."""

        abstract = True
