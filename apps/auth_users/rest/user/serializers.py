from rest_framework import serializers
from django.contrib.auth.hashers import make_password

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


PASSWORD_DEFAULT_PROPERTY = {"min_length": 8, "max_length": 255}


class UserCreateAndUpdateBaseSerializer(serializers.ModelSerializer):
    password = PasswordField(**PASSWORD_DEFAULT_PROPERTY)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")

    def create(self, validated_data: dict[str, str]) -> User:
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    def update(self, user: User, validated_data: dict[str, str]) -> User:
        user.username = validated_data.get("username", user.username)
        user.email = validated_data.get("email", user.email)
        user.first_name = validated_data.get("first_name", user.first_name)
        user.last_name = validated_data.get("last_name", user.last_name)

        validated_password = validated_data.get("password")

        if validated_password:
            user.set_password(validated_password)

        user.save()

        return user


class UserCreateSerializer(UserCreateAndUpdateBaseSerializer):
    pass


class UserUpdateSerializer(UserCreateAndUpdateBaseSerializer):
    password = PasswordField(**PASSWORD_DEFAULT_PROPERTY, required=False)
