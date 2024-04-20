from django.db import models

from calls.models.mixins import UuidMixin


class OperatorSubscriber(UuidMixin, models.Model):
    operator = models.ForeignKey("Operator", models.CASCADE)
    subscriber = models.ForeignKey("Subscriber", models.CASCADE)

    def __str__(self) -> str:
        return f"{self.operator.title} - {self.subscriber.full_name}"

    class Meta:
        unique_together = ("operator", "subscriber")
