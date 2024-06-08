"""Async consumer helper module."""

from typing import Optional, cast

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from django.contrib.auth.models import AnonymousUser
from subscribers.models import Subscriber


class AsyncConsumerHelper(AsyncJsonWebsocketConsumer):
    """Async consumer helper.

    Args:
        AsyncJsonWebsocketConsumer: Standard class from django-channels.
    """

    unique_prefix: str
    subscriber: Subscriber

    def get_channel_layer(self) -> InMemoryChannelLayer:
        """Get channel layer.

        Returns:
            InMemoryChannelLayer: Channel layer.
        """
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_subscriber(self) -> Optional[Subscriber]:
        """Get subscriber by the django request.

        Returns:
            Optional[Subscriber]: The given subscriber from the django request.
        """
        subscriber = cast(Subscriber | AnonymousUser, self.scope["user"])

        if isinstance(subscriber, AnonymousUser):
            return None

        return subscriber

    def create_unique(self, subscriber_id: str) -> str:
        """Create a unique subscriber id group name.

        Args:
            subscriber_id: The given subscriber id.

        Returns:
            str: The created subscriber id group name.
        """
        return f"{self.unique_prefix}_{subscriber_id}"

    def set_subscriber(self, subscriber: Subscriber) -> None:
        """Set subscriber.

        Args:
            subscriber: The given subscriber.
        """
        self.subscriber = subscriber
