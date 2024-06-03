"""Subscriber view set module."""

from pathlib import PurePath
from typing import cast

from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from subscribers.models import Subscriber

from .permissions import SubscriberPermission
from .serializers import (SubscriberCreateAndUpdateSerializer,
                          SubscriberDefaultSerializer,
                          SubscriberExtendedDefaultSerializer)


class SubscriberViewSet(viewsets.ModelViewSet):
    """Subscriber view set class."""

    queryset = Subscriber.objects.all()
    permission_classes = (SubscriberPermission,)

    def get_serializer_class(self):
        """Get serializer class.

        Returns:
            Never: Never.
        """
        match self.request.method:
            case "POST" | "PUT" | "PATCH":
                self.serializer_class = SubscriberCreateAndUpdateSerializer
            case _:
                current_subscriber = cast(Subscriber | AnonymousUser, self.request.user)

                if isinstance(current_subscriber, AnonymousUser):
                    self.serializer_class = SubscriberDefaultSerializer
                    return super().get_serializer_class()

                url_subscriber_id = PurePath(self.request.path).parts[-1]

                is_staff = current_subscriber.is_staff
                is_current_user = str(current_subscriber.id) == url_subscriber_id

                self.serializer_class = (
                    SubscriberExtendedDefaultSerializer
                    if is_staff or is_current_user
                    else SubscriberDefaultSerializer
                )

        return super().get_serializer_class()
