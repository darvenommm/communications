from django.db import models
from django.utils.translation import gettext_lazy as _

from library.models.mixins.uuid_mixin import UuidMixin
from library.models.mixins.created_mixin import CreatedMixin
from library.models.mixins.updated_mixin import UpdatedMixin
from library.models.validators.time_range_validator import TimeRangeValidator

from subscribers.models import Subscriber


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    title_max_length = 100
    description_max_length = 2500

    title = models.CharField(_("title"), max_length=title_max_length, unique=True, db_index=True)
    foundation_date = models.DateField(_("foundation date"), validators=(TimeRangeValidator(),))
    description = models.CharField(
        _("description"),
        max_length=description_max_length,
        blank=True,
        default="",
    )

    subscribers = models.ManyToManyField(
        Subscriber,
        blank=True,
        through="OperatorSubscriber",
        verbose_name=_("subscribers"),
        related_name="operators",
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        db_table = '"communications"."operator"'
        verbose_name = _("operator")
        verbose_name_plural = _("operators")
        ordering = ("title", "foundation_date")
