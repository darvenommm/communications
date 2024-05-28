from datetime import date, datetime
from typing import Optional, NoReturn, Self, TypeAlias

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.utils.timezone import get_current_timezone


TimeRangeType: TypeAlias = date | datetime


@deconstructible
class TimeRangeValidator:
    def __init__(
        self, start: Optional[TimeRangeType] = None, end: Optional[TimeRangeType] = None
    ) -> None:
        self.__start = start
        self.__end = end

    def __call__(self, given_date: TimeRangeType) -> None | NoReturn:
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
        return (self.start == other.start) and (self.end == other.start)

    @property
    def start(self) -> Optional[TimeRangeType]:
        return self.__start

    @property
    def end(self) -> Optional[TimeRangeType]:
        return self.__end
