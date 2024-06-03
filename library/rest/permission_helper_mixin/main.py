"""Rest framework permission helper mixin module."""

from rest_framework import permissions
from rest_framework.request import HttpRequest


class PermissionHelperMixin:
    """Rest framework permission helper mixin."""

    def is_staff(self, request: HttpRequest) -> bool:
        """Check is user staff.

        Args:
            request: Django request.

        Returns:
            bool: Is user staff?
        """
        return bool(request.user and getattr(request.user, "is_staff", False))

    def is_safe_method(self, request: HttpRequest) -> bool:
        """Check does the django request have a safe method.

        Args:
            request: Django request.

        Returns:
            bool: Does the django request have a safe method?
        """
        return request.method in permissions.SAFE_METHODS

    def is_staff_or_safe_method(self, request: HttpRequest) -> bool:
        """Check is user staff or does the django request have a safe method.

        Args:
            request: Django request.

        Returns:
            bool: Is user staff or does the django request have a safe method?
        """
        return self.is_staff(request) or self.is_safe_method(request)
