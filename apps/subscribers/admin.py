from django.contrib import admin
from django.contrib.auth.models import Group as GroupBase
from rest_framework.authtoken.admin import TokenAdmin
from django.utils.translation import gettext_lazy as _

from .admin_models import SubscriberAdmin
from .models import Subscriber


admin.site.unregister(GroupBase)


@admin.site.register
class Group(GroupBase):
    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")
        proxy = True


TokenAdmin.raw_id_fields = ("user",)
admin.register(Subscriber)(SubscriberAdmin)
