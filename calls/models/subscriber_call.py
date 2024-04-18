from django.db import models

from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin
from . import subscriber as s


class SubscriberCall(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    caller = models.ForeignKey(s.Subscriber, on_delete=models.CASCADE, related_name="made_calls")
    receiver = models.ForeignKey(
        s.Subscriber, on_delete=models.CASCADE, related_name="received_calls"
    )
    start = models.DateTimeField()
    duration = models.PositiveIntegerField()  # in seconds

    class Meta:
        ordering = ["caller__full_name", "receiver__full_name"]
