from rest_framework import permissions, request, viewsets

from calls.models import Operator
from library.PermissionHelperMixin import PermissionHelperMixin


class OperatorPermission(PermissionHelperMixin, permissions.BasePermission):
    def has_permission(self, request: request.HttpRequest, view: viewsets.ModelViewSet):
        if self.is_admin_or_safe_method(request):
            return True

        return view.detail

    def has_object_permission(
        self, request: request.HttpRequest, _: viewsets.ModelViewSet, __: Operator
    ):
        return self.is_admin_or_safe_method(request)
