from rest_framework import permissions, request, viewsets

from library.PermissionHelperMixin import PermissionHelperMixin
from calls.models import Subscriber


class SubscriberPermission(PermissionHelperMixin, permissions.BasePermission):
    def has_permission(self, request: request.HttpRequest, view: viewsets.ModelViewSet):
        if self.is_staff(request):
            return True

        request_method: str = getattr(request, "method")

        if request_method in (*permissions.SAFE_METHODS, "POST"):
            return True

        return view.detail

    def has_object_permission(
        self, request: request.HttpRequest, _: viewsets.ModelViewSet, subscriber: Subscriber
    ):
        if self.is_staff_or_safe_method(request):
            return True

        return request.user == subscriber.user
