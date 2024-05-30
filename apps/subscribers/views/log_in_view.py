from django import forms
from django.contrib.auth import forms, views


class LogInView(views.LoginView):
    form_class = forms.AuthenticationForm
    template_name = "subscribers/pages/log_in.html"
