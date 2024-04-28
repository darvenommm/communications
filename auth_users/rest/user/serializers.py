from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from auth_users.models import User


class UserReadSerializer(serializers.ModelSerializer):
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


class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)


class PasswordField(serializers.CharField):
    def to_representation(self, _):
        return ""


class UserCreateSerializer(serializers.ModelSerializer):
    password = PasswordField(max_length=255, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])

        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = PasswordField(required=False, max_length=255, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name")

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
