from typing import cast
from django.db import models
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from subscribers.models import Subscriber
from calls.models import SubscriberCall


class CallsHistoryView(LoginRequiredMixin, ListView):
    context_object_name = "calls"
    template_name = "calls/pages/calls_history.html"

    def get_queryset(self) -> models.QuerySet[SubscriberCall]:
        subscriber_id = str(cast(Subscriber, self.request.user).id)

        self.queryset = SubscriberCall.objects.filter(
            models.Q(caller_id=subscriber_id) | models.Q(receiver_id=subscriber_id)
        )

        return super().get_queryset()
