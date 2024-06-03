"""Registration admin models module."""

from django.contrib import admin
from django.contrib.auth.models import Group as GroupBase
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.admin import TokenAdmin

from .admin_models import SubscriberAdmin
from .models import Subscriber

admin.site.unregister(GroupBase)


@admin.site.register
class Group(GroupBase):
    """Group admin class."""

    class Meta:
        """Class Meta."""

        verbose_name = _("group")
        verbose_name_plural = _("groups")
        proxy = True


TokenAdmin.raw_id_fields = ("user",)
admin.register(Subscriber)(SubscriberAdmin)
