from django.db import models
from rest_framework import viewsets, permissions

from calls.models import SubscriberCall
from .permissions import SubscriberCallPermission
from .serializers import (
    SubscriberCallReadSerializer,
    SubscriberCallDeleteSerializer,
    SubscriberCallCreateAndUpdateSerializer,
)


class SubscriberCallViewSet(viewsets.ModelViewSet):
    queryset = SubscriberCall.objects.select_related("caller__user", "receiver__user").all()
    permission_classes = (permissions.IsAuthenticated, SubscriberCallPermission)

    def filter_queryset(self, queryset: models.QuerySet):
        if getattr(self.request.user, "is_staff", False):
            return super().filter_queryset(queryset)

        user_pk = getattr(self.request.user, "pk")
        queryset = queryset.filter(
            models.Q(caller__user__pk=user_pk) | models.Q(receiver__user__pk=user_pk)
        )

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = SubscriberCallCreateAndUpdateSerializer
            case "DELETE":
                self.serializer_class = SubscriberCallDeleteSerializer
            case _:
                self.serializer_class = SubscriberCallReadSerializer

        return super().get_serializer_class()
