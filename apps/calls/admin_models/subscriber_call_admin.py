from typing import Any

from calls.models import SubscriberCall
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SubscriberCallForm(forms.ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        if cleaned_data.get("caller") == cleaned_data.get("receiver"):
            raise ValidationError(
                _("The fields caller and receiver can't be equal"),
                code="invalid",
            )

        return cleaned_data

    class Meta:
        model = SubscriberCall
        fields = ("caller", "receiver", "start", "duration")


class SubscriberCallAdmin(admin.ModelAdmin):
    form = SubscriberCallForm

    search_fields = (
        "caller__first_name__startswith",
        "caller__last_name__startswith",
        "receiver__first_name__startswith",
        "receiver__last_name__startswith",
    )

    list_per_page = 25
    list_display = ("caller", "receiver", "start", "duration")
    list_display_links = ("caller", "receiver")
