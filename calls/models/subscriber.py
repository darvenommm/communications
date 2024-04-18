from django.db import models
from django.core.validators import RegexValidator

from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin
from calls.models.functions import ConcatString


class Subscriber(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    class Meta:
        ordering = ["first_name", "last_name", "birth_date"]

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    full_name = models.GeneratedField(  # type: ignore
        expression=ConcatString("first_name", " ", "last_name"),
        output_field=models.TextField(),
        db_persist=True,
    )
    birth_date = models.DateField()
    passport_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Incorrect passport number format")],
        unique=True,
    )

    def __str__(self) -> str:
        return self.full_name
