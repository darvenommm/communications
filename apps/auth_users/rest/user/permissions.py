from typing import cast

from rest_framework import permissions, viewsets, request

from library.PermissionHelperMixin import PermissionHelperMixin
from auth_users.models import User


class UserPermission(PermissionHelperMixin, permissions.BasePermission):
    def has_permission(self, request: request.Request, view: viewsets.ModelViewSet):
        if self.is_staff(request):
            return True

        return view.detail

    def has_object_permission(self, request: request.Request, _: viewsets.ModelViewSet, user: User):
        if self.is_staff(request):
            return True

        return request.user == user
