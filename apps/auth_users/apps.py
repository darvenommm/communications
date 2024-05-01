from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuthUsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "auth_users"
    verbose_name = _("users")
