from typing import Any, cast, Optional

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, request

from auth_users.models import User


class UserDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
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


class PasswordField(serializers.CharField):
    def to_representation(self, _):
        return ""


class UserCreateAndUpdateSerializer(serializers.ModelSerializer):
    password_min_length = 8
    password_max_length = 255

    password = PasswordField(
        min_length=password_min_length,
        max_length=password_max_length,
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

    def validate(self, user_data: dict[str, Any]) -> dict[str, Any]:
        self.validate_password(cast(Optional[str], user_data.get("password")))
        return super().validate(user_data)

    def validate_password(self, password: Optional[str]) -> str:
        incorrect_password_length_message = _(
            "Incorrect password length (min: %(min)s, max: %(max)s)"
            % {"min": self.password_min_length, "max": self.password_max_length},
        )

        if cast(request.HttpRequest, self.context.get("request")).method == "POST":
            if password is None:
                raise ValidationError({"password": _("You didn't send a password value!")})

            if not (self.password_min_length <= len(password) <= self.password_max_length):
                raise ValidationError({"password": incorrect_password_length_message})
        else:
            password = cast(str, password)

        return password

    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, user: User, validated_data: dict[str, Any]) -> User:
        user.username = validated_data.get("username", user.username)
        user.email = validated_data.get("email", user.email)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)

        validated_password = validated_data.get("password")

        if validated_password:
            user.set_password(validated_password)

        user.save()

        return user
