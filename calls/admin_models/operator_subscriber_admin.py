from django.contrib import admin


class OperatorSubscriberAdmin(admin.ModelAdmin):
    search_fields = ("operator__title__startswith", "subscriber__full_name__startswith")

    list_per_page = 25
    list_display = ("operator", "subscriber")
    list_display_links = ("operator", "subscriber")

    fieldsets = (
        (
            "Operator - Subscriber fields",
            {
                "fields": ("operator", "subscriber"),
            },
        ),
    )
