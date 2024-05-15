from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView

from calls.models import Subscriber


class SubscribersView(ListView):
    queryset = (
        Subscriber.objects.select_related("user")
        .prefetch_related("operators")
        .only("user__id", "user__full_name", "user__username", "operators")
    )
    context_object_name = "subscribers"
    template_name = "calls/pages/subscribers.html"
