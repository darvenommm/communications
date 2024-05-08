from django.db import models
from rest_framework import viewsets, permissions

from calls.models import SubscriberCall
from .permissions import SubscriberCallPermission
from .serializers import SubscriberCallDefaultSerializer, SubscriberCallCreateAndUpdateSerializer


class SubscriberCallViewSet(viewsets.ModelViewSet):
    queryset = SubscriberCall.objects.select_related("caller__user", "receiver__user").all()
    permission_classes = (permissions.IsAuthenticated, SubscriberCallPermission)

    def filter_queryset(self, queryset: models.QuerySet):
        if getattr(self.request.user, "is_staff", False):
            return super().filter_queryset(queryset)

        user_pk = getattr(self.request.user, "pk")
        queryset = queryset.filter(
            models.Q(caller__user_id=user_pk) | models.Q(receiver__user_id=user_pk)
        )

        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = SubscriberCallCreateAndUpdateSerializer
            case _:
                self.serializer_class = SubscriberCallDefaultSerializer

        return super().get_serializer_class()
