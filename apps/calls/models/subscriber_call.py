"""Subscriber call model module."""

from django.db import models
from django.utils.translation import gettext_lazy as _
from subscribers.models import Subscriber

from library.models.mixins.created_mixin import CreatedMixin
from library.models.mixins.updated_mixin import UpdatedMixin
from library.models.mixins.uuid_mixin import UuidMixin
from library.models.validators.duration_positivity_validator import duration_positivity_validator
from library.models.validators.time_range_validator import TimeRangeValidator


class SubscriberCall(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    """Subscriber call model."""

    caller = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="made_calls",
        verbose_name=_("caller"),
    )
    receiver = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        related_name="received_calls",
        verbose_name=_("call receiver"),
    )
    start = models.DateTimeField(_("start time"), validators=(TimeRangeValidator(),))
    duration = models.DurationField(_("duration"), validators=(duration_positivity_validator,))

    def __str__(self) -> str:
        """Get string presentation.

        Returns:
            str: string presentation.
        """
        return _("call from %(caller_full_name)s to %(receiver_full_name)s") % {
            "caller_full_name": self.caller.full_name,
            "receiver_full_name": self.receiver.full_name,
        }

    class Meta:
        """Class Meta."""

        verbose_name = _("subscriber call")
        verbose_name_plural = _("subscribers calls")
        db_table = '"communications"."subscriber_call"'
        ordering = (
            "caller__first_name",
            "caller__last_name",
            "receiver__first_name",
            "receiver__last_name",
        )
        constraints = (
            models.CheckConstraint(
                check=~models.Q(caller_id=models.F("receiver_id")),  # not equal
                name="check_not_equal_caller_and_receiver",
            ),
        )
