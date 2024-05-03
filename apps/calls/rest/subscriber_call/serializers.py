from typing import Any

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from calls.models import SubscriberCall, Subscriber
from calls.rest.subscriber import SubscriberReadSerializer


class SubscriberCallReadSerializer(serializers.ModelSerializer):
    caller = SubscriberReadSerializer()
    receiver = SubscriberReadSerializer()

    class Meta:
        model = SubscriberCall
        fields = ("id", "caller", "receiver", "start", "duration")


class SubscriberCallDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberCall
        fields = ("id",)


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
        fields = ("id", "caller", "receiver", "start", "duration")
