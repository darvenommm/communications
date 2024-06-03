"""Subscriber serializers."""

from typing import Any, Optional, cast

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import request, serializers
from subscribers.models import Subscriber

public_subscriber_fields = (
    "id",
    "username",
    "email",
    "first_name",
    "last_name",
    "full_name",
    "date_joined",
    "last_login",
    "is_active",
    "is_staff",
)


class SubscriberDefaultSerializer(serializers.ModelSerializer):
    """Default subscriber serializer."""

    class Meta:
        """Class Meta."""

        model = Subscriber
        fields = public_subscriber_fields


class SubscriberExtendedDefaultSerializer(serializers.ModelSerializer):
    """Subscriber extended default serializer."""

    class Meta:
        """Class Meta."""

        model = Subscriber
        fields = (*public_subscriber_fields, "passport", "birth_date")


class PasswordField(serializers.CharField):
    """Password Field."""

    def to_representation(self, _):
        """Get presentation.

        Args:
            _: Value.

        Returns:
            _: "".
        """
        return ""


class SubscriberCreateAndUpdateSerializer(serializers.ModelSerializer):
    """Subscriber serializer for creating and updating."""

    password = PasswordField(
        min_length=Subscriber.password_min_length,
        max_length=Subscriber.passport_max_length,
        required=False,
    )

    class Meta:
        """Class Meta."""

        model = Subscriber
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "passport",
            "birth_date",
        )

    def validate(self, subscriber_data: dict[str, Any]) -> dict[str, Any]:
        """Validate subscriber's data.

        Args:
            subscriber_data: Subscriber's data.

        Returns:
            dict[str, Any]: the given data.
        """
        self.validate_password(cast(Optional[str], subscriber_data.get("password")))
        return super().validate(subscriber_data)

    def validate_password(self, password: Optional[str]) -> Optional[str]:
        """Validate password.

        Args:
            password: The given password.

        Raises:
            ValidationError: Incorrect password.

        Returns:
            Optional[str]: password.
        """
        sent_empty_password_message = _("You send empty password for creating new a subscriber!")
        received_request = cast(request.HttpRequest, self.context.get("request"))

        if (received_request.method == "POST") and (password is None):
            raise ValidationError({"password": sent_empty_password_message}, "incorrect_password")

        return password

    def create(self, validated_data: dict[str, Any]) -> Subscriber:
        """Create a subscriber.

        Args:
            validated_data: The given validation data.

        Returns:
            Subscriber: created subscriber.
        """
        password = validated_data.pop("password")
        subscriber = Subscriber(**validated_data)
        subscriber.set_password(password)
        subscriber.save()

        return subscriber

    def update(self, subscriber: Subscriber, validated_data: dict[str, Any]) -> Subscriber:
        """Update subscriber.

        Args:
            subscriber: The given subscriber.
            validated_data: The validation data.

        Returns:
            Subscriber: updated subscriber.
        """
        subscriber.username = validated_data.get("username", subscriber.username)
        subscriber.email = validated_data.get("email", subscriber.email)
        subscriber.first_name = validated_data.get("first_name", subscriber.first_name)
        subscriber.last_name = validated_data.get("last_name", subscriber.last_name)
        subscriber.passport = validated_data.get("passport", subscriber.passport)
        subscriber.birth_date = validated_data.get("birth_date", subscriber.birth_date)

        validated_password = validated_data.get("password")

        if validated_password:
            subscriber.set_password(validated_password)

        subscriber.save()

        return subscriber
