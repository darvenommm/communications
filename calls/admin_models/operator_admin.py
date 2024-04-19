from django.contrib import admin

from calls.models import OperatorSubscriber


class SubscriberInline(admin.TabularInline):
    model = OperatorSubscriber
    fields = ("subscriber",)
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith",)

    list_per_page = 25
    list_display = ("title", "foundation_date")

    inlines = (SubscriberInline,)

    fieldsets = (
        (
            "Operator fields",
            {
                "fields": ("title", "description", "foundation_date"),
            },
        ),
    )
