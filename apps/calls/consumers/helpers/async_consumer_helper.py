from typing import cast

from django.contrib.auth.models import AnonymousUser
from channels.layers import InMemoryChannelLayer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from subscribers.models import Subscriber


class AsyncConsumerHelper(AsyncJsonWebsocketConsumer):
    unique_prefix: str

    def get_channel_layer(self) -> InMemoryChannelLayer:
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_subscriber(self) -> Subscriber:
        subscriber = cast(Subscriber | AnonymousUser, self.scope["user"])

        if isinstance(subscriber, AnonymousUser):
            raise ValueError("Current subscriber doesn't authorized!")

        return subscriber

    def create_unique(self, subscriber_id: str) -> str:
        return f"{self.unique_prefix}_{subscriber_id}"
