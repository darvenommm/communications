from rest_framework import permissions, request


class PermissionChecker:
    def is_admin(self, request: request.HttpRequest) -> bool:
        return bool(request.user and getattr(request.user, "is_staff", False))

    def is_safe(self, request: request.HttpRequest) -> bool:
        return request.method in permissions.SAFE_METHODS

    def is_admin_or_safe(self, request: request.HttpRequest) -> bool:
        return self.is_admin(request) or self.is_safe(request)
