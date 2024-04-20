from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class OperatorSubscriberAdmin(admin.ModelAdmin):
    search_fields = ("operator__title__startswith", "subscriber__full_name__startswith")

    list_per_page = 25
    list_display = ("operator", "subscriber")
    list_display_links = ("operator", "subscriber")

    fieldsets = (
        (
            _("operator - subscriber fields"),
            {
                "fields": ("operator", "subscriber"),
            },
        ),
    )
