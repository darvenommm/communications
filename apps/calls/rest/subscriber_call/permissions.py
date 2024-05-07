from rest_framework import permissions, request, viewsets

from library.PermissionHelperMixin import PermissionHelperMixin
from calls.models import SubscriberCall


class SubscriberCallPermission(PermissionHelperMixin, permissions.BasePermission):
    def has_permission(self, request: request.Request, view: viewsets.ModelViewSet):
        if self.is_staff_or_safe_method(request):
            return True

        return view.detail

    def has_object_permission(
        self, request: request.Request, _: viewsets.ModelViewSet, call: SubscriberCall
    ):
        if self.is_staff(request):
            return True

        if not self.is_safe_method(request):
            return False

        return request.user.pk in (call.caller.user.pk, call.receiver.user.pk)
