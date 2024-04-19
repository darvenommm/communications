from django.contrib import admin

from calls.models import OperatorSubscriber


class OperatorInline(admin.TabularInline):
    model = OperatorSubscriber
    fields = ("operator",)
    extra = 1


class SubscriberAdmin(admin.ModelAdmin):
    search_fields = ("first_name__startswith", "last_name__startswith")

    list_per_page = 30
    list_display = ("first_name", "last_name", "birth_date", "passport")
    list_display_links = ("first_name", "last_name")

    inlines = (OperatorInline,)

    fieldsets = (
        (
            "Subscriber fields",
            {
                "fields": ("first_name", "last_name", "birth_date", "passport"),
            },
        ),
    )
