"""Subscriber permissions."""

from rest_framework import permissions, viewsets
from rest_framework.request import HttpRequest
from subscribers.models import Subscriber

from library.rest.permission_helper_mixin import PermissionHelperMixin


class SubscriberPermission(PermissionHelperMixin, permissions.BasePermission):
    """Subscriber permission class."""

    def has_permission(self, _: HttpRequest, view: viewsets.ModelViewSet) -> bool:
        """Has permission.

        Args:
            _: HttpRequest.
            view: ModelViewSet.

        Returns:
            bool: has access.
        """
        if not view.detail:
            return True

        return view.detail

    def has_object_permission(
        self,
        request: HttpRequest,
        _: viewsets.ModelViewSet,
        subscriber: Subscriber,
    ) -> bool:
        """Has permission.

        Args:
            request: HttpRequest.
            _: ModelViewSet.
            subscriber: The current subscriber.

        Returns:
            bool: has access.
        """
        if self.is_staff_or_safe_method(request):
            return True

        return request.user == subscriber
