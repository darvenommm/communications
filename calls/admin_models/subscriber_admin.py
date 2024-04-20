from django.contrib import admin

from calls.models import OperatorSubscriber


class OperatorInline(admin.StackedInline):
    model = OperatorSubscriber
    fields = ("operator",)
    extra = 1


class SubscriberAdmin(admin.ModelAdmin):
    search_fields = ("first_name__startswith", "last_name__startswith")

    list_per_page = 25
    list_display = ("first_name", "last_name", "birth_date", "passport")
    list_display_links = ("first_name", "last_name")

    inlines = (OperatorInline,)
    list_filter = ("operators",)

    fieldsets = (
        (
            "Subscriber fields",
            {
                "fields": ("first_name", "last_name", "birth_date", "passport"),
            },
        ),
    )
