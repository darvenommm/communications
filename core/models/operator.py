from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models.mixins import UuidMixin, CreatedMixin, UpdatedMixin


TITLE_MAX_LENGTH = 100


class Operator(UuidMixin, CreatedMixin, UpdatedMixin, models.Model):
    title = models.CharField(_("title"), max_length=TITLE_MAX_LENGTH, unique=True, db_index=True)
    description = models.TextField(_("description"), blank=True, default="")
    foundation_date = models.DateField(_("foundation date"))

    subscribers = models.ManyToManyField(
        "Subscriber",
        blank=True,
        through="OperatorSubscriber",
        related_name="+",
        verbose_name=_("subscribers"),
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = _("mobile operator")
        verbose_name_plural = _("mobile operators")
        ordering = ["title", "foundation_date"]
