"""Call urls."""

from django.urls import path, reverse_lazy
from django.views.generic import RedirectView, TemplateView

from .views import CallsHistoryView, ChoosingOperatorsView, SubscribersView

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("home"), permanent=True)),
    path("subscribers/", SubscribersView.as_view(), name="home"),
    path("calls-history/", CallsHistoryView.as_view(), name="calls_history"),
    path("choosing-operators/", ChoosingOperatorsView.as_view(), name="choosing_operators"),
    path(
        "call-room/<uuid:call_room_id>/",
        TemplateView.as_view(template_name="calls/pages/call_room.html"),
        name="call_room",
    ),
]
