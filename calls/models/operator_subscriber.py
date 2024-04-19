from django.db import models

from calls.models.mixins import UuidMixin


class OperatorSubscriber(UuidMixin, models.Model):
    operator = models.ForeignKey("Operator", models.CASCADE)
    subscriber = models.ForeignKey("Subscriber", models.CASCADE)
