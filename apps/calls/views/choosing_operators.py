from typing import cast

from django import forms
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from subscribers.models import Subscriber
from calls.forms import ChoosingOperatorsForm


class ChoosingOperatorsView(LoginRequiredMixin, FormView):
    template_name = "calls/pages/choosing_operators.html"
    form_class = ChoosingOperatorsForm
    success_url = reverse_lazy("home")

    def form_valid(self, form: forms.Form):
        subscriber = cast(Subscriber, self.request.user)
        operators = getattr(subscriber, "operators")
        operators.clear()
        operators.add(*form.clean()["operators"])
        return super().form_valid(form)
