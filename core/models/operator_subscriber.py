from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.mixins import UuidMixin


class OperatorSubscriber(UuidMixin, models.Model):
    operator = models.ForeignKey("Operator", models.CASCADE, verbose_name=_("operator"))
    subscriber = models.ForeignKey("Subscriber", models.CASCADE, verbose_name=_("subscriber"))

    def __str__(self) -> str:
        return f"{self.operator.title} - {self.subscriber.full_name}"

    class Meta:
        verbose_name = _("relation of operator and subscriber")
        verbose_name_plural = _("relations of operator and subscriber")
        db_table = '"mobile_communications"."operator_subscriber"'
        unique_together = ("operator", "subscriber")
