from django.db import models

from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


TITLE_MAX_LENGTH = 100


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    foundation_date = models.DateField()

    subscribers = models.ManyToManyField(
        "Subscriber",
        blank=True,
        through="OperatorSubscriber",
        related_name="+",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title", "foundation_date"]
