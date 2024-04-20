from django.db import models
from django.core.validators import RegexValidator

from calls.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin
from calls.models.functions import ConcatString


FIRST_NAME_MAX_LENGTH = 64
LAST_NAME_MAX_LENGTH = 64
PASSPORT_MAX_LENGTH = 10

PASSPORT_REGEX = r"^\d{%s}$" % PASSPORT_MAX_LENGTH

INCORRECT_PASSPORT_MESSAGE = "Incorrect passport number format"


class Subscriber(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)
    full_name: str = models.GeneratedField(  # type: ignore
        expression=ConcatString("first_name", models.Value(" "), "last_name"),
        output_field=models.CharField(
            max_length=(FIRST_NAME_MAX_LENGTH + LAST_NAME_MAX_LENGTH + 1)
        ),
        db_persist=True,
    )
    birth_date = models.DateField()
    passport = models.CharField(
        max_length=PASSPORT_MAX_LENGTH,
        validators=[RegexValidator(PASSPORT_REGEX, INCORRECT_PASSPORT_MESSAGE)],
        unique=True,
    )

    operators = models.ManyToManyField(
        "Operator",
        blank=True,
        through="OperatorSubscriber",
        related_name="+",
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name", "birth_date"]
