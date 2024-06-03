"""Subscriber call view set module."""

from calls.models import SubscriberCall
from django.db import models
from rest_framework import permissions, viewsets

from .permissions import SubscriberCallPermission
from .serializers import SubscriberCallCreateAndUpdateSerializer, SubscriberCallDefaultSerializer


class SubscriberCallViewSet(viewsets.ModelViewSet):
    """Subscriber call view set."""

    queryset = SubscriberCall.objects.select_related("caller", "receiver").all()
    permission_classes = (permissions.IsAuthenticated, SubscriberCallPermission)

    def filter_queryset(self, queryset: models.QuerySet) -> models.QuerySet[SubscriberCall]:
        """Filter queryset.

        Args:
            queryset: The given queryset.

        Returns:
            models.QuerySet[SubscriberCall]: Filtered queryset.
        """
        if getattr(self.request.user, "is_staff", False):
            return super().filter_queryset(queryset)

        user_pk = self.request.user.pk
        queryset = queryset.filter(models.Q(caller_id=user_pk) | models.Q(receiver_id=user_pk))

        return super().filter_queryset(queryset)

    def get_serializer_class(self) -> None:
        """Get serializer class.

        Returns:
            None: None.
        """
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = SubscriberCallCreateAndUpdateSerializer
            case _:
                self.serializer_class = SubscriberCallDefaultSerializer

        return super().get_serializer_class()
