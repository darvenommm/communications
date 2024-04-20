from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


class SubscriberCall(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    caller = models.ForeignKey(
        "Subscriber",
        on_delete=models.CASCADE,
        related_name="made_calls",
        verbose_name=_("caller"),
    )
    receiver = models.ForeignKey(
        "Subscriber",
        on_delete=models.CASCADE,
        related_name="received_calls",
        verbose_name=_("call receiver"),
    )
    start = models.DateTimeField(_("start time"))
    duration = models.DurationField(_("duration"))

    def __str__(self) -> str:
        return _("call from %(caller_full_name)s to %(receiver_full_name)s") % {
            "caller_full_name": self.caller.full_name,
            "receiver_full_name": self.receiver.full_name,
        }

    class Meta:
        verbose_name = _("subscriber call")
        verbose_name_plural = _("subscribers calls")
        ordering = ["start", "caller__full_name", "receiver__full_name"]
        constraints = (
            models.CheckConstraint(
                check=~models.Q(caller_id=models.F("receiver_id")),  # not equal
                name="check_not_equal_caller_and_receiver",
            ),
        )
