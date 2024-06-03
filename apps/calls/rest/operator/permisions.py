"""Operator permission module."""

from calls.models import Operator
from rest_framework import permissions, viewsets
from rest_framework.request import HttpRequest

from library.rest.permission_helper_mixin import PermissionHelperMixin


class OperatorPermission(PermissionHelperMixin, permissions.BasePermission):
    """Operator permission."""

    def has_permission(self, request: HttpRequest, view: viewsets.ModelViewSet) -> bool:
        """Check permission.

        Args:
            request: HttpRequest.
            view: ModelViewSet.

        Returns:
            bool: Does user have a permission.
        """
        if self.is_staff_or_safe_method(request):
            return True

        return bool(view.detail)

    def has_object_permission(
        self,
        request: HttpRequest,
        view: viewsets.ModelViewSet,
        operator: Operator,
    ) -> bool:
        """Check permission.

        Args:
            request: HttpRequest.
            view: ModelViewSet.
            operator: The given Operator.

        Returns:
            bool: Does user have a permission.
        """
        return self.is_staff_or_safe_method(request)
