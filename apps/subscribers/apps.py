from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscribersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "subscribers"
    verbose_name = _("subscribers")
