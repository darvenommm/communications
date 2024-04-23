from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext_lazy as _


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
