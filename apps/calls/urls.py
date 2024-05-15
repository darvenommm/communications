from django.urls import path

from .views import SubscribersView


app_name = "calls"

urlpatterns = [
    path("subscribers/", SubscribersView.as_view(), name="subscribers"),
]
