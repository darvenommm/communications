from django.contrib import admin
from django.contrib.auth.models import Group as BaseGroup

from .admin_models import UserAdmin
from .models import User


admin.site.unregister(BaseGroup)


@admin.site.register
class Group(BaseGroup):
    class Meta:
        proxy = True


admin.register(User)(UserAdmin)
