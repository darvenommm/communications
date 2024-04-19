from django.contrib import admin


class SubscriberCallAdmin(admin.ModelAdmin):
    search_fields = (
        "caller__first_name__startswith",
        "caller__last_name__startswith",
        "receiver__first_name__startswith",
        "receiver__last_name__startswith",
    )

    list_per_page = 30
    list_display = ("caller", "receiver", "start", "duration")
    list_display_links = ("caller", "receiver")

    fieldsets = (
        (
            "Subscriber call fields",
            {
                "fields": ("caller", "receiver", "start", "duration"),
            },
        ),
    )
