from uuid import UUID
from typing import Any, cast

from django.contrib.auth import get_user_model, hashers
from rest_framework import serializers, validators, request

from calls.models import Subscriber, Operator
from auth_users.rest import UserDefaultSerializer, UserCreateAndUpdateSerializer

from calls.rest.operator import OperatorDefaultSerializer


class SubscriberDefaultSerializer(serializers.ModelSerializer):
    user = UserDefaultSerializer()
    operators = OperatorDefaultSerializer(many=True)

    class Meta:
        model = Subscriber
        fields = ("id", "birth_date", "user", "operators")
        depth = 1


class SubscriberExtendedDefaultSerializer(SubscriberDefaultSerializer):
    class Meta:
        model = Subscriber
        fields = ("id", "birth_date", "passport", "user", "operators")
        depth = 1


class SubscriberCreateSerializer(serializers.ModelSerializer):
    user = UserCreateAndUpdateSerializer()
    operators = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Operator.objects.all(),
        required=False,
    )

    class Meta:
        model = Subscriber
        fields = ("birth_date", "passport", "user", "operators")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if cast(request.HttpRequest, self.context.get("request")).method not in ("PUT", "PATCH"):
            return

        user_serializer = cast(UserCreateAndUpdateSerializer, self.fields["user"])
        username_field = cast(serializers.CharField, user_serializer.fields["username"])
        new_username_validators = []

        for username_validator in username_field.validators:
            if isinstance(username_validator, validators.UniqueValidator):
                parsed_path = filter(
                    bool, cast(request.HttpRequest, self.context["request"]).path.split("/")
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

    def create(self, validated_data: dict[str, Any]) -> Subscriber:
        user_request_data = cast(dict[str, str], validated_data.pop("user"))
        user_data = {
            "username": user_request_data["username"],
            "first_name": user_request_data["first_name"],
            "last_name": user_request_data["last_name"],
            "email": user_request_data["email"],
            "password": hashers.make_password(user_request_data["password"]),
        }

        user = get_user_model().objects.create(**user_data)

        operators = cast(list, validated_data.pop("operators"))

        subscriber = Subscriber.objects.create(user=user, **validated_data)
        subscriber.operators.add(*operators)

        return subscriber

    def update(self, subscriber: Subscriber, validated_data: dict[str, Any]) -> Subscriber:
        user = subscriber.user
        user_data = cast(dict[str, str], validated_data.pop("user"))
        user_password = user_data.get("password")

        user.username = user_data.get("username", user.username)
        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)

        if user_password:
            user.set_password(user_password)

        user.save()

        subscriber.passport = validated_data.get("passport", subscriber.passport)
        subscriber.birth_date = validated_data.get("birth_date", subscriber.birth_date)

        if subscriber.operators:
            subscriber.operators.clear()
            subscriber.operators.add(*validated_data["operators"])

        subscriber.save()

        return subscriber
