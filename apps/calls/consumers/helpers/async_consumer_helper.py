from typing import cast

from django.contrib.auth.models import AnonymousUser
from channels.layers import InMemoryChannelLayer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from auth_users.models import User


class AsyncConsumerHelper(AsyncJsonWebsocketConsumer):
    def get_channel_layer(self) -> InMemoryChannelLayer:
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_user(self) -> User:
        user = cast(User | AnonymousUser, self.scope["user"])
        is_authorized_user = hasattr(user, "id")

        if not is_authorized_user:
            raise ValueError("Isn't user authorized!")

        return cast(User, user)
