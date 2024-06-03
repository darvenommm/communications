"""Log in view module."""

from django.contrib.auth import forms, views


class LogInView(views.LoginView):
    """Log in view class."""

    form_class = forms.AuthenticationForm
    template_name = "subscribers/pages/log_in.html"
