from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from core.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin
from core.models.functions import ConcatString


FIRST_NAME_MAX_LENGTH = 64
LAST_NAME_MAX_LENGTH = 64
PASSPORT_MAX_LENGTH = 11

PASSPORT_REGEX = r"^\d{4}-\d{6}$"

INCORRECT_PASSPORT_MESSAGE = _('incorrect passport number format (example: "0000-000000")')
PASSPORT_HELP_TEXT = _('Passport number has a format like "0000-000000"')


class Subscriber(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    first_name = models.CharField(_("first name"), max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(_("last name"), max_length=LAST_NAME_MAX_LENGTH)
    full_name: str = models.GeneratedField(  # type: ignore
        expression=ConcatString("first_name", models.Value(" "), "last_name"),
        output_field=models.CharField(
            max_length=(FIRST_NAME_MAX_LENGTH + LAST_NAME_MAX_LENGTH + 1)
        ),
        db_persist=True,
    )
    birth_date = models.DateField(_("birth day"))
    passport = models.CharField(
        _("passport number"),
        max_length=PASSPORT_MAX_LENGTH,
        validators=[RegexValidator(PASSPORT_REGEX, INCORRECT_PASSPORT_MESSAGE)],
        unique=True,
        help_text=PASSPORT_HELP_TEXT,
    )

    operators = models.ManyToManyField(
        "Operator",
        blank=True,
        through="OperatorSubscriber",
        related_name="+",
        verbose_name=_("operators"),
    )

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = _("subscriber")
        verbose_name_plural = _("subscribers")
        db_table = '"mobile_communications"."subscriber"'
        ordering = ("first_name", "last_name", "birth_date")
