from typing import cast

from django.contrib.auth.models import AbstractUser
from rest_framework import permissions, request, viewsets


class OperatorPermission(permissions.BasePermission):
    def is_admin(self, request: request.HttpRequest) -> bool:
        return bool(request.user and cast(AbstractUser, request.user).is_staff)

    def has_permission(self, request: request.HttpRequest, view: viewsets.ModelViewSet):
        if self.is_admin(request):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return view.detail

    def has_object_permission(self, request, view, obj):
        if self.is_admin(request):
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False
