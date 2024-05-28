from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from subscribers.models import Subscriber


class RegistrationForm(forms.ModelForm):
    repeated_password = forms.CharField(max_length=Subscriber.password_max_length, required=True)

    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        repeated_password = cleaned_data.get("repeated_password")

        if password and repeated_password and (password != repeated_password):
            raise ValidationError(
                _("Password and repeated password have to be equal"), code="incorrect_password"
            )

        return cleaned_data

    class Meta:
        model = Subscriber
        fields = ("first_name", "last_name", "username", "password", "repeated_password")
