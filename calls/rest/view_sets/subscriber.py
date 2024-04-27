from typing import cast

from django.http.request import HttpRequest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers, viewsets, permissions

from calls.models import Subscriber, Operator
from auth_users.export.types import UserType

# from auth_users.export.rest import UserSerializer


class SubscriberPermission(permissions.BasePermission):
    def is_admin(self, request: HttpRequest) -> bool:
        return bool(request.user and cast(UserType, request.user).is_staff)

    def has_permission(self, request: HttpRequest, view: viewsets.ModelViewSet):
        if self.is_admin(request):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return view.detail

    def has_object_permission(
        self, request: HttpRequest, _: viewsets.ModelViewSet, subscriber: Subscriber
    ):
        if self.is_admin(request):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == subscriber.user


class OperatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ("id", "title", "description", "foundation_date")
