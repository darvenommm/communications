from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from subscribers.models import Subscriber
from subscribers.rest.subscriber import SubscriberDefaultSerializer
from calls.models import SubscriberCall


class SubscriberCallDefaultSerializer(serializers.ModelSerializer):
    caller = SubscriberDefaultSerializer()
    receiver = SubscriberDefaultSerializer()

    class Meta:
        model = SubscriberCall
        fields = ("id", "caller", "receiver", "start", "duration")


class SubscriberCallCreateAndUpdateSerializer(serializers.ModelSerializer):
    caller = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all())

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        if attrs["caller"] == attrs["receiver"]:
            raise ValidationError(
                {"caller_and_receiver": _("Caller and receiver should be different!")},
                code="invalid",
            )

        return super().validate(attrs)

    class Meta:
        model = SubscriberCall
        fields = ("caller", "receiver", "start", "duration")
