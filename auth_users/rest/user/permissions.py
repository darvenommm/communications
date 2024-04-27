from typing import cast

from django.http.request import HttpRequest
from rest_framework import permissions, viewsets

from auth_users.models import User


class UserPermission(permissions.BasePermission):
    def is_admin(self, request: HttpRequest) -> bool:
        return bool(request.user and cast(User, request.user).is_staff)

    def has_permission(self, request: HttpRequest, view: viewsets.ModelViewSet):
        if self.is_admin(request):
            return True

        return view.detail

    def has_object_permission(self, request: HttpRequest, _: viewsets.ModelViewSet, user: User):
        if self.is_admin(request):
            return True

        return request.user == user
