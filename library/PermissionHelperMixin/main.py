from rest_framework import permissions, request


class PermissionHelperMixin:
    def is_staff(self, request: request.Request) -> bool:
        return bool(request.user and getattr(request.user, "is_staff", False))

    def is_safe_method(self, request: request.Request) -> bool:
        return request.method in permissions.SAFE_METHODS

    def is_staff_or_safe_method(self, request: request.Request) -> bool:
        return self.is_staff(request) or self.is_safe_method(request)
