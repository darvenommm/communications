from datetime import date
from typing import cast

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

from auth_users.export.types import UserType

from .mixins import UuidMixin, CreatedMixin, UpdatedMixin
from .validators import TimeRangeValidator


PASSPORT_MAX_LENGTH = 11
PASSPORT_REGEX = r"^\d{4}-\d{6}$"
INCORRECT_PASSPORT_MESSAGE = _('incorrect passport number format (example: "0000-000000")')
PASSPORT_HELP_TEXT = _('Passport number has a format like "0000-000000"')


class Subscriber(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    user = cast(
        models.OneToOneField[UserType],
        models.OneToOneField(
            get_user_model(),
            on_delete=models.CASCADE,
            related_name="subscriber",
            unique=True,
        ),
    )

    passport = models.CharField(
        _("passport number"),
        max_length=PASSPORT_MAX_LENGTH,
        validators=(RegexValidator(PASSPORT_REGEX, INCORRECT_PASSPORT_MESSAGE),),
        unique=True,
        help_text=PASSPORT_HELP_TEXT,
    )
    birth_date = models.DateField(
        _("birth day"),
        validators=(TimeRangeValidator(start=date(1920, 1, 1)),),
    )

    operators = models.ManyToManyField(
        "Operator",
        blank=True,
        through="OperatorSubscriber",
        related_name="+",
        verbose_name=_("operators"),
    )

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = _("subscriber")
        verbose_name_plural = _("subscribers")
        db_table = '"communications"."subscriber"'
        ordering = ("user__full_name", "birth_date")
