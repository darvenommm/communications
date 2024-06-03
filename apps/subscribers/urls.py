"""Subscribers urls."""

from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import LogInView, RegistrationView

app_name = "auth"

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("log-in/", LogInView.as_view(), name="log_in"),
    path("log-out/", LogoutView.as_view(), name="log_out"),
]
