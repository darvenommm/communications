from django.views.generic import ListView

from subscribers.models import Subscriber


class SubscribersView(ListView):
    queryset = Subscriber.objects.prefetch_related("operators").only(
        "id", "first_name", "last_name", "username", "operators"
    )
    context_object_name = "subscribers"
    template_name = "calls/pages/subscribers.html"
