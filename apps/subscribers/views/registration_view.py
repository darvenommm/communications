from django.views.generic import FormView
from django.forms import ModelForm
from django.http.response import HttpResponse
from django.urls import reverse_lazy

from subscribers.forms import RegistrationForm
from subscribers.models import Subscriber


class RegistrationView(FormView):
    success_url = reverse_lazy("calls:home")
    template_name = "subscribers/registration.html"
    form_class = RegistrationForm

    def form_valid(self, form: ModelForm) -> HttpResponse:
        cleaned_data = form.clean()
        (password, _) = (cleaned_data.pop("password"), cleaned_data.pop("repeated_password"))

        new_user = Subscriber(**cleaned_data)
        new_user.set_password(password)

        new_user.save()

        return super().form_valid(form)
