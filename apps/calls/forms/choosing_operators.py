"""Choosing operators form module."""

from calls.models import Operator
from django import forms


class ChoosingOperatorsForm(forms.Form):
    """Choosing operators form."""

    operators = forms.ModelMultipleChoiceField(
        queryset=Operator.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        """Class Meta."""

        fields = ("operators",)
