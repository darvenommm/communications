"""Operator admin module."""

from calls.models import OperatorSubscriber
from django.contrib import admin


class SubscribersInlineAdmin(admin.StackedInline):
    """Subscriber inline admin."""

    model = OperatorSubscriber
    fields = ("subscriber",)
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    """Operator admin."""

    search_fields = ("title__startswith",)

    list_per_page = 25
    list_display = ("title", "foundation_date")

    inlines = (SubscribersInlineAdmin,)

    fields = ("title", "description", "foundation_date")
