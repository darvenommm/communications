"""Subscriber serializers."""

from typing import Any

from calls.models import SubscriberCall
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from subscribers.models import Subscriber
from subscribers.rest.subscriber import SubscriberDefaultSerializer


class SubscriberCallDefaultSerializer(serializers.ModelSerializer):
    """Subscriber call default serializer."""

    caller = SubscriberDefaultSerializer()
    receiver = SubscriberDefaultSerializer()

    class Meta:
        """Class Meta."""

        model = SubscriberCall
        fields = ("id", "caller", "receiver", "start", "duration")


class SubscriberCallCreateAndUpdateSerializer(serializers.ModelSerializer):
    """Subscriber call serializer for creating and updating."""

    caller = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all())

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        """Validate gotten attributes.

        Args:
            attrs: The gotten attributes.

        Raises:
            ValidationError: Caller and receiver are equal.

        Returns:
            dict[str, Any]: The gotten attributes.
        """
        if attrs["caller"] == attrs["receiver"]:
            raise ValidationError(
                {"caller_and_receiver": _("Caller and receiver should be different!")},
                code="invalid",
            )

        return super().validate(attrs)

    class Meta:
        """Class Meta."""

        model = SubscriberCall
        fields = ("caller", "receiver", "start", "duration")
