from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def duration_positivity_validator(duration: timedelta):
    if duration <= timedelta(0):
        raise ValidationError(
            _("%(duration_value)s is not a valid duration. It must be positive.")
            % {"duration_value": duration},
        )
