"""Time range validator module."""

from datetime import date, datetime
from typing import Optional, Self, TypeAlias

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.timezone import get_current_timezone
from django.utils.translation import gettext_lazy as _

TimeRangeType: TypeAlias = date | datetime


@deconstructible
class TimeRangeValidator:
    """Time range validator class."""

    def __init__(
        self,
        start: Optional[TimeRangeType] = None,
        end: Optional[TimeRangeType] = None,
    ) -> None:
        """Init time range validator.

        Args:
            start: start time. Defaults to None.
            end: end time. Defaults to None.
        """
        self.__start = start
        self.__end = end

    def __call__(self, given_date: TimeRangeType) -> None:
        """Call method.

        Args:
            given_date: given data from django.

        Raises:
            ValidationError: given data is smaller than start time.
            ValidationError: given data is bigger than end time.
        """
        end = self.end

        if not end:
            end = (
                datetime.today().astimezone(get_current_timezone())
                if isinstance(given_date, datetime)
                else date.today()
            )

        if self.start and given_date < self.start:
            raise ValidationError(
                _("Given time should be after %(start)s!"),
                code="invalid_time",
                params={"start": str(self.start)},
            )

        if end < given_date:
            raise ValidationError(
                _("Given time should be before %(end)s!"),
                code="invalid_time",
                params={
                    "end": str(end),
                },
            )

    def __eq__(self, other: Self) -> bool:
        """Check are they equal.

        Args:
            other: other given data.

        Returns:
            bool: Are they equal?
        """
        return (self.start == other.start) and (self.end == other.start)

    @property
    def start(self) -> Optional[TimeRangeType]:
        """Get start time value.

        Returns:
            Optional[TimeRangeType]: start time.
        """
        return self.__start

    @property
    def end(self) -> Optional[TimeRangeType]:
        """Get end time value.

        Returns:
            Optional[TimeRangeType]: end time.
        """
        return self.__end
