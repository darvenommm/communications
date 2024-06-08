"""Calls config module."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CallsConfig(AppConfig):
    """Calls config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "calls"
    verbose_name = _("communication via calls")
