from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SubscriberCallAdmin(admin.ModelAdmin):
    search_fields = (
        "caller__first_name__startswith",
        "caller__last_name__startswith",
        "receiver__first_name__startswith",
        "receiver__last_name__startswith",
    )

    list_per_page = 25
    list_display = ("caller", "receiver", "start", "duration")
    list_display_links = ("caller", "receiver")

    fieldsets = (
        (
            _("subscriber call fields"),
            {
                "fields": ("caller", "receiver", "start", "duration"),
            },
        ),
    )
