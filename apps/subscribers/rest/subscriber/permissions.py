from rest_framework import permissions, viewsets, request

from library.rest.permission_helper_mixin import PermissionHelperMixin
from subscribers.models import Subscriber


class SubscriberPermission(PermissionHelperMixin, permissions.BasePermission):
    def has_permission(self, _: request.HttpRequest, view: viewsets.ModelViewSet):
        if not view.detail:
            return True

        return view.detail

    def has_object_permission(
        self, request: request.HttpRequest, _: viewsets.ModelViewSet, subscriber: Subscriber
    ):
        if self.is_staff_or_safe_method(request):
            return True

        return request.user == subscriber
