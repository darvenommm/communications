"""Subscriber call permission module."""

from calls.models import SubscriberCall
from rest_framework import permissions, viewsets
from rest_framework.request import HttpRequest

from library.rest.permission_helper_mixin import PermissionHelperMixin


class SubscriberCallPermission(PermissionHelperMixin, permissions.BasePermission):
    """Subscriber call permission."""

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
        _: viewsets.ModelViewSet,
        call: SubscriberCall,
    ) -> bool:
        """Check permission.

        Args:
            request: HttpRequest.
            _: ModelViewSet.
            call: Given subscriber call.

        Returns:
            bool: Does user have a permission.
        """
        if self.is_staff(request):
            return True

        if not self.is_safe_method(request):
            return False

        ids = (call.caller.id, call.receiver.id)

        return request.user.pk in ids
