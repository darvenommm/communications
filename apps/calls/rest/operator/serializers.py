"""Operators serializers."""

from calls.models import Operator
from rest_framework import serializers


class OperatorDefaultSerializer(serializers.ModelSerializer):
    """Operator default serializer."""

    class Meta:
        """Class Meta."""

        model = Operator
        fields = ("id", "title", "description", "foundation_date")


class OperatorChangeAndUpdateSerializer(serializers.ModelSerializer):
    """Operator serializer for creating and updating."""

    class Meta:
        """Class Meta."""

        model = Operator
        fields = ("title", "description", "foundation_date")
