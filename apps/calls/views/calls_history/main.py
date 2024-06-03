"""Call history view module."""

from typing import cast

from calls.models import SubscriberCall
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.views.generic import ListView
from subscribers.models import Subscriber


class CallsHistoryView(LoginRequiredMixin, ListView):
    """Call history view."""

    context_object_name = "calls"
    template_name = "calls/pages/calls_history.html"

    def get_queryset(self) -> models.QuerySet[SubscriberCall]:
        """Get queryset.

        Returns:
            models.QuerySet[SubscriberCall]: The gotten queryset.
        """
        subscriber_id = str(cast(Subscriber, self.request.user).id)

        self.queryset = SubscriberCall.objects.filter(
            models.Q(caller_id=subscriber_id) | models.Q(receiver_id=subscriber_id),
        )

        return super().get_queryset()
