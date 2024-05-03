from typing import cast

from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets

from calls.models import Subscriber
from .permissions import SubscriberPermission
from .serializers import (
    SubscriberReadSerializer,
    SubscriberReadExtendedSerializer,
    SubscriberCreateSerializer,
    SubscriberUpdateSerializer,
    SubscriberDeleteSerializer,
)


class SubscriberViewSet(viewsets.ModelViewSet):
    queryset = Subscriber.objects.select_related("user").prefetch_related("operators").all()
    permission_classes = (SubscriberPermission,)

    def get_serializer_class(self):
        match self.request.method:
            case "POST":
                self.serializer_class = SubscriberCreateSerializer
            case "PUT" | "PATCH":
                self.serializer_class = SubscriberUpdateSerializer
            case "DELETE":
                self.serializer_class = SubscriberDeleteSerializer
            case _:
                user = self.request.user
                is_staff = cast(bool, getattr(user, "is_staff"))

                if not isinstance(user, AnonymousUser) and getattr(user, "subscriber", False):
                    current_subscriber_pk = str(cast(Subscriber, getattr(user, "subscriber")).pk)
                else:
                    current_subscriber_pk = ""

                current_page_subscriber_pk = list(filter(bool, self.request.path.split("/")))[-1]
                is_current_user = current_subscriber_pk == current_page_subscriber_pk

                self.serializer_class = (
                    SubscriberReadExtendedSerializer
                    if is_staff or is_current_user
                    else SubscriberReadSerializer
                )

        return super().get_serializer_class()

    def perform_destroy(self, subscriber: Subscriber):
        subscriber.user.delete()

        return super().perform_destroy(subscriber)
