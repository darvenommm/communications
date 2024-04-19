from django.db import models

from . import subscriber as s
from . import operator_subscriber as o_s
from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


TITLE_MAX_LENGTH = 100


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    class Meta:
        ordering = ["title", "foundation_date"]

    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    foundation_date = models.DateField()

    subscribers = models.ManyToManyField(
        "Subscriber",
        blank=True,
        through="OperatorSubscriber",
        related_name="operators",
    )

    def __str__(self) -> str:
        return self.title
