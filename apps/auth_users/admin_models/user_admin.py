from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token


class TokenStackedInline(admin.StackedInline):
    model = Token


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            _("user fields"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    inlines = (TokenStackedInline,)
