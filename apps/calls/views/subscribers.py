from django.views.generic import ListView

from calls.models import Subscriber


class SubscribersView(ListView):
    queryset = (
        Subscriber.objects.select_related("user")
        .prefetch_related("operators")
        .only("user__id", "user__first_name", "user__last_name", "user__username", "operators")
    )
    context_object_name = "subscribers"
    template_name = "calls/pages/subscribers.html"
