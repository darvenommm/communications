from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from calls.models import OperatorSubscriber


class SubscribersInlineAdmin(admin.StackedInline):
    model = OperatorSubscriber
    fields = ("subscriber",)
    extra = 1


class OperatorAdmin(admin.ModelAdmin):
    search_fields = ("title__startswith",)

    list_per_page = 25
    list_display = ("title", "foundation_date")

    inlines = (SubscribersInlineAdmin,)

    fields = ("title", "description", "foundation_date")
