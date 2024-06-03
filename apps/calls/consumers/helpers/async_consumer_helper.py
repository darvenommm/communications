from typing import Optional, cast

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from django.contrib.auth.models import AnonymousUser
from subscribers.models import Subscriber


class AsyncConsumerHelper(AsyncJsonWebsocketConsumer):
    unique_prefix: str
    subscriber: Subscriber

    def get_channel_layer(self) -> InMemoryChannelLayer:
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_subscriber(self) -> Optional[Subscriber]:
        subscriber = cast(Subscriber | AnonymousUser, self.scope["user"])

        if isinstance(subscriber, AnonymousUser):
            return

        return subscriber

    def create_unique(self, subscriber_id: str) -> str:
        return f"{self.unique_prefix}_{subscriber_id}"

    def set_subscriber(self, subscriber: Subscriber) -> None:
        self.subscriber = subscriber
