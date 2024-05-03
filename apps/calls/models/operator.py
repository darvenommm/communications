from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import TimeRangeValidator
from .mixins import UuidMixin, CreatedMixin, UpdatedMixin


TITLE_MAX_LENGTH = 100
DESCRIPTION_MAX_LENGTH = 2500


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    title = models.CharField(_("title"), max_length=TITLE_MAX_LENGTH, unique=True, db_index=True)
    foundation_date = models.DateField(_("foundation date"), validators=(TimeRangeValidator(),))
    description = models.CharField(
        _("description"),
        max_length=DESCRIPTION_MAX_LENGTH,
        blank=True,
        default="",
    )

    subscribers = models.ManyToManyField(
        "Subscriber",
        blank=True,
        through="OperatorSubscriber",
        verbose_name=_("subscribers"),
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("operator")
        verbose_name_plural = _("operators")
        db_table = '"communications"."operator"'
        ordering = ("title", "foundation_date")
