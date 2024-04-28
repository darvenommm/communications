from rest_framework import permissions, request, viewsets

from calls.rest.mixins.permissions import PermissionChecker
from calls.models import Subscriber


class SubscriberPermission(PermissionChecker, permissions.BasePermission):
    def has_permission(self, request: request.HttpRequest, view: viewsets.ModelViewSet):
        if self.is_admin(request):
            return True

        if request.method in (*permissions.SAFE_METHODS, "POST"):
            return True

        return view.detail

    def has_object_permission(
        self, request: request.HttpRequest, _: viewsets.ModelViewSet, subscriber: Subscriber
    ):
        if self.is_admin_or_safe(request):
            return True

        return request.user == subscriber.user
