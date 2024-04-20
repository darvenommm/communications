from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.models import OperatorSubscriber


class SubscribersInlineAdmin(admin.StackedInline):
    model = OperatorSubscriber
    fields = ("subscriber",)
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith",)

    list_per_page = 25
    list_display = ("title", "foundation_date")

    inlines = (SubscribersInlineAdmin,)

    fieldsets = (
        (
            _("operator fields"),
            {
                "fields": ("title", "description", "foundation_date"),
            },
        ),
    )
