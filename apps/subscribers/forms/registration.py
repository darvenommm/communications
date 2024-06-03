"""Registration form module."""

from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from subscribers.models import Subscriber


class RegistrationForm(forms.ModelForm):
    """Registration form."""

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )
    repeated_password = forms.CharField(
        widget=forms.PasswordInput,
        max_length=Subscriber.password_max_length,
        strip=False,
    )

    def clean(self) -> dict[str, Any]:
        """Validate the given data.

        Raises:
            ValidationError: Passwords aren't equal.

        Returns:
            dict[str, Any]: The cleaned data.
        """
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        repeated_password = cleaned_data.get("repeated_password")

        if password and repeated_password and (password != repeated_password):
            raise ValidationError(
                _("Password and repeated password have to be equal"),
                code="incorrect_password",
            )

        return cleaned_data

    class Meta:
        """Class Meta."""

        model = Subscriber
        fields = (
            "first_name",
            "last_name",
            "username",
            "password",
            "repeated_password",
            "passport",
            "birth_date",
        )
