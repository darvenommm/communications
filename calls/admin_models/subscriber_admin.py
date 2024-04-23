from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from calls.models import OperatorSubscriber


class OperatorInline(admin.StackedInline):
    model = OperatorSubscriber
    fields = ("operator",)
    extra = 1


class SubscriberAdmin(admin.ModelAdmin):
    search_fields = ("user__full_name__startswith",)

    list_per_page = 25
    list_display = ("user", "birth_date", "passport")
    list_display_links = ("user",)

    inlines = (OperatorInline,)
    list_filter = ("operators",)

    fieldsets = (
        (
            _("user"),
            {
                "fields": ("user",),
            },
        ),
        (
            _("subscriber fields"),
            {
                "fields": ("birth_date", "passport"),
            },
        ),
    )
