from typing import cast
import datetime

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _

from library.models.mixins.uuid_mixin import UuidMixin
from library.models.validators.time_range_validator import TimeRangeValidator


INCORRECT_PASSPORT_MESSAGE = _('incorrect passport number format (example: "0000-000000")')
PASSPORT_HELP_TEXT = _('Passport number has a format like "0000-000000"')


class Subscriber(UuidMixin, AbstractUser):
    first_name_max_length = 150
    last_name_max_length = 150
    username_max_length = 150
    password_min_length = 8
    password_max_length = 128
    passport_max_length = 11
    passport_regex = r"^\d{4}-\d{6}$"

    first_name = models.CharField(_("first name"), max_length=first_name_max_length)
    last_name = models.CharField(_("last name"), max_length=last_name_max_length)
    passport = models.CharField(
        _("passport number"),
        max_length=passport_max_length,
        validators=(RegexValidator(passport_regex, INCORRECT_PASSPORT_MESSAGE),),
        unique=True,
        null=True,
        blank=True,
        help_text=PASSPORT_HELP_TEXT,
    )
    birth_date = models.DateField(
        _("birth day"),
        validators=(TimeRangeValidator(start=datetime.date(1920, 1, 1)),),
        blank=True,
        null=True,
    )

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    def __str__(self) -> str:
        full_name = cast(str, self.full_name).strip()

        # By default in the db has one user with empty first and last name, it's a admin 99.9%
        return f"{self.full_name if full_name else _('admin')}"

    class Meta:
        verbose_name = _("subscriber")
        verbose_name_plural = _("subscribers")
        db_table = '"communications"."subscriber"'
        ordering = ("first_name", "last_name", "birth_date")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
