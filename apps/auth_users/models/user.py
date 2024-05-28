from uuid import uuid4
from typing import cast

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name_max_length = 150
    last_name_max_length = 150
    username_max_length = 150
    password_max_length = 128

    id = models.UUIDField(primary_key=True, default=uuid4)
    first_name = models.CharField(_("first name"), max_length=first_name_max_length, blank=False)
    last_name = models.CharField(_("last name"), max_length=last_name_max_length, blank=False)

    @property
    def full_name(self) -> str:
        return self.get_username()

    def __str__(self) -> str:
        full_name = cast(str, self.full_name).strip()

        # By default in the db has one user with empty first and last name, it's a admin 99.9%
        return f"{self.full_name if full_name else _('admin')}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
