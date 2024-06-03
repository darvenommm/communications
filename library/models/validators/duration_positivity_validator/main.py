"""Duration positivity validator module."""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def duration_positivity_validator(duration: timedelta) -> None:
    """Check duration positivity.

    Args:
        duration: The given duration.

    Raises:
        ValidationError: Incorrect given duration.
    """
    if duration <= timedelta(0):
        raise ValidationError(
            _("%(duration_value)s is not a valid duration. It must be positive.")
            % {"duration_value": duration},
        )
