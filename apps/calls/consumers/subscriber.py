import json
from uuid import UUID
from typing import Any, cast, Literal

from django.contrib.auth.models import AbstractUser, AnonymousUser

from channels.layers import InMemoryChannelLayer
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class SubscriberConsumer(AsyncJsonWebsocketConsumer):
    group_name = "online-subscribers"
    active_users: dict[str, Literal[True]] = {}

    def get_channel_layer(self) -> InMemoryChannelLayer:
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_user_id(self) -> UUID | None:
        user = cast(AnonymousUser | AbstractUser, self.scope["user"])

        return cast(UUID | None, getattr(user, "id", None))

    async def connect(self) -> None:
        await self.get_channel_layer().group_add(self.group_name, self.channel_name)

        user_id = self.get_user_id()

        if user_id:
            user_id = str(user_id)

            self.active_users[user_id] = True
            await self.get_channel_layer().group_send(
                self.group_name,
                {"type": "notify_inviting_new_subscriber", "subscriber_id": user_id},
            )

        await self.accept()

    async def disconnect(self, _: int) -> None:
        await self.get_channel_layer().group_discard(self.group_name, self.channel_name)

        user_id = self.get_user_id()

        if user_id:
            user_id = str(user_id)

            del self.active_users[user_id]
            await self.get_channel_layer().group_send(
                self.group_name, {"type": "notify_uninviting_subscriber", "subscriber_id": user_id}
            )

    async def receive(self, text_data: str) -> None:
        given_data = cast(dict[str, Any], json.loads(text_data))

        match given_data.get("type"):
            case "get_online_subscribers":
                await self.get_online_subscribers()

    async def get_online_subscribers(self) -> None:
        await self.send_json(
            {
                "type": "get_online_subscribers",
                "data": json.dumps(self.active_users),
            }
        )

    async def notify_inviting_new_subscriber(self, event: dict[str, str]) -> None:
        await self.send_json(
            {
                "type": "notify_inviting_new_subscriber",
                "data": event["subscriber_id"],
            }
        )

    async def notify_uninviting_subscriber(self, event: dict[str, str]) -> None:
        await self.send_json(
            {
                "type": "notify_uninviting_subscriber",
                "data": event["subscriber_id"],
            }
        )
