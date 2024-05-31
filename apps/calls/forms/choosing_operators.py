from typing import Any
from django import forms

from calls.models import Operator


class ChoosingOperatorsForm(forms.Form):
    operators = forms.ModelMultipleChoiceField(
        queryset=Operator.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        fields = ("operators",)
