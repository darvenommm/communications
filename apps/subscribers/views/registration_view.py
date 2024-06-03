"""Registration view module."""

from django.forms import ModelForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from subscribers.forms import RegistrationForm
from subscribers.models import Subscriber


class RegistrationView(FormView):
    """Registration view class."""

    template_name = "subscribers/pages/registration.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """Save subscriber to the db.

        Args:
            form: The given form.

        Returns:
            HttpResponse: Django response.
        """
        cleaned_data = form.clean()
        (password, _) = (cleaned_data.pop("password"), cleaned_data.pop("repeated_password"))

        new_user = Subscriber(**cleaned_data)
        new_user.set_password(password)

        new_user.save()

        return super().form_valid(form)
