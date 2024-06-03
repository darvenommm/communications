"""Choosing operators view module."""

from typing import Any, cast

from calls.forms import ChoosingOperatorsForm
from django import forms
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView
from subscribers.models import Subscriber


class ChoosingOperatorsView(LoginRequiredMixin, FormView):
    """Choosing operators view."""

    template_name = "calls/pages/choosing_operators.html"
    form_class = ChoosingOperatorsForm
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """Get context data.

        Args:
            kwargs: Extra keyword arguments.

        Returns:
            dict[str, Any]: The updated context data.
        """
        extra_content = super().get_context_data(**kwargs)
        user = cast(Subscriber, self.request.user)
        operators = user.operators  # type: ignore

        return {**extra_content, "operators": operators.all()}

    def form_valid(self, form: forms.Form) -> HttpResponse:
        """Add operators after form validating.

        Args:
            form: The given form

        Returns:
            HttpResponse: The django response.
        """
        subscriber = cast(Subscriber, self.request.user)
        operators = subscriber.operators  # type: ignore
        operators.clear()
        operators.add(*form.clean()["operators"])
        return super().form_valid(form)
