"""Operator subscriber model module."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from subscribers.models import Subscriber

from library.models.mixins.uuid_mixin import UuidMixin

from .operator import Operator


class OperatorSubscriber(UuidMixin, models.Model):
    """Operator subscriber model."""

    operator = models.ForeignKey(Operator, models.CASCADE, verbose_name=_("operator"))
    subscriber = models.ForeignKey(Subscriber, models.CASCADE, verbose_name=_("subscriber"))

    def __str__(self) -> str:
        """Get string presentation.

        Returns:
            str: string presentation.
        """
        return f"{self.operator.title} - {self.subscriber.full_name}"

    class Meta:
        """Class Meta."""

        verbose_name = _("relation of operator and subscriber")
        verbose_name_plural = _("relations of operator and subscriber")
        db_table = '"communications"."operator_subscriber"'
        unique_together = ("operator", "subscriber")
