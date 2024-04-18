from django.db import models

from . import subscriber as s
from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    class Meta:
        ordering = ["title", "foundation_date"]

    title = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, default="")
    foundation_date = models.DateField()
    subscribers = models.ManyToManyField(s.Subscriber, related_name="operators")

    def __str__(self) -> str:
        return self.title
