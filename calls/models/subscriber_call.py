from django.db import models

from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


class SubscriberCall(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    caller = models.ForeignKey("Subscriber", on_delete=models.CASCADE, related_name="made_calls")
    receiver = models.ForeignKey(
        "Subscriber", on_delete=models.CASCADE, related_name="received_calls"
    )
    start = models.DateTimeField()
    duration = models.DurationField()

    def __str__(self) -> str:
        return f"Call from {self.caller.full_name} to {self.receiver.full_name}"

    class Meta:
        ordering = ["start", "caller__full_name", "receiver__full_name"]
        constraints = (
            models.CheckConstraint(
                check=~models.Q(caller_id=models.F("receiver_id")),  # not equal
                name="check_not_equal_caller_and_receiver",
            ),
        )
