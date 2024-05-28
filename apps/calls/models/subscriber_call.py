from django.db import models
from django.utils.translation import gettext_lazy as _

from .mixins import UuidMixin, CreatedMixin, UpdatedMixin
from .validators import duration_positivity_validator, TimeRangeValidator
from .subscriber import Subscriber


class SubscriberCall(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
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
        return _("call from %(caller_full_name)s to %(receiver_full_name)s") % {
            "caller_full_name": self.caller.user.full_name,
            "receiver_full_name": self.receiver.user.full_name,
        }

    class Meta:
        verbose_name = _("subscriber call")
        verbose_name_plural = _("subscribers calls")
        db_table = '"communications"."subscriber_call"'
        ordering = (
            "caller__user__first_name",
            "caller__user__last_name",
            "receiver__user__first_name",
            "receiver__user__last_name",
        )
        constraints = (
            models.CheckConstraint(
                check=~models.Q(caller_id=models.F("receiver_id")),  # not equal
                name="check_not_equal_caller_and_receiver",
            ),
        )
