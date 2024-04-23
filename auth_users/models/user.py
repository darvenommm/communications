from typing import cast

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .functions import ConcatString
from .types import GeneratedFieldsType


FIRST_NAME_MAX_LENGTH = 150
LAST_NAME_MAX_LENGTH = 150


class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=FIRST_NAME_MAX_LENGTH, blank=False)
    last_name = models.CharField(_("last name"), max_length=LAST_NAME_MAX_LENGTH, blank=False)

    full_name = cast(GeneratedFieldsType, getattr(models, "GeneratedField"))(
        expression=ConcatString("first_name", models.Value(" "), "last_name"),
        output_field=models.TextField(),
        db_persist=True,
    )

    def __str__(self) -> str:
        # admin by default no have first and last names -> empty string with one space
        full_name = cast(str, self.full_name).strip()

        return f"{self.full_name if full_name else _('admin')}"
