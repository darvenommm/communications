from typing import Any, cast
from uuid import UUID

from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, validators

from calls.models import Subscriber, Operator
from auth_users.export.rest import (
    UserReadSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)


class OperatorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date")


class SubscriberReadSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    operators = OperatorReadSerializer(many=True)

    class Meta:
        model = Subscriber
        fields = ("id", "birth_date", "user", "operators")
        depth = 1


class SubscriberReadExtendedSerializer(serializers.ModelSerializer):
    user = UserReadSerializer()
    operators = OperatorReadSerializer(many=True)

    class Meta:
        model = Subscriber
        fields: tuple[str, ...] = ("id", "birth_date", "passport", "user", "operators")
        depth = 1


class SubscriberDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ("id",)


class SubscriberCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    operators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Operator.objects.all(), required=False
    )

    class Meta:
        model = Subscriber
        fields = ("id", "birth_date", "passport", "user", "operators")

    def create(self, validated_data: dict[str, Any]) -> Subscriber:
        user_request_data = cast(dict[str, str], validated_data.pop("user"))
        user_data = {
            "username": user_request_data["username"],
            "first_name": user_request_data["first_name"],
            "last_name": user_request_data["last_name"],
            "email": user_request_data["email"],
            "password": make_password(user_request_data["password"]),
        }

        user = get_user_model().objects.create(**user_data)
        operators = cast(list, validated_data.pop("operators"))

        subscriber = Subscriber.objects.create(user=user, **validated_data)
        subscriber.operators.add(*operators)

        return subscriber


class SubscriberUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()
    operators = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Operator.objects.all(),
        required=False,
    )

    # fix unique validator for username fields
    # If you're in your subscriber page you can't not change your username
    # because you're getting text hint it should be unique username
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user_serializer = cast(UserUpdateSerializer, self.fields["user"])
        username_field = cast(serializers.CharField, user_serializer.fields["username"])
        username_validators = username_field.validators
        new_username_validators = []

        for username_validator in username_validators:
            if isinstance(username_validator, validators.UniqueValidator):
                parsed_path = filter(
                    bool, cast(HttpRequest, self.context["request"]).path.split("/")
                )
                subscriber_pk = UUID(list(parsed_path)[-1])

                new_username_validators.append(
                    validators.UniqueValidator(
                        queryset=get_user_model().objects.exclude(subscriber__pk=subscriber_pk)
                    )
                )
            else:
                new_username_validators.append(username_validator)

        self.fields["user"].fields["username"].validators = new_username_validators

    class Meta:
        model = Subscriber
        fields = ("id", "passport", "birth_date", "user", "operators")

    def update(self, subscriber: Subscriber, validated_data: dict[str, Any]) -> Subscriber:
        user = subscriber.user
        user_data = cast(dict[str, str], validated_data.pop("user"))
        user_password = user_data.get("password")

        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.password = make_password(user_password) if user_password else user.password
        user.save()

        subscriber.passport = validated_data.get("passport", subscriber.passport)
        subscriber.birth_date = validated_data.get("birth_date", subscriber.birth_date)

        if subscriber.operators:
            subscriber.operators.clear()
            subscriber.operators.add(*validated_data["operators"])

        subscriber.save()
        return subscriber
