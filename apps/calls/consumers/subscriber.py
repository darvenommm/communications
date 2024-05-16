import json
from typing import Any, cast, Callable, Coroutine, Literal, Optional
from enum import StrEnum

from django.contrib.auth.models import AnonymousUser

from channels.layers import InMemoryChannelLayer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from auth_users.models import User


class ActionType(StrEnum):
    subscribers_online = "subscribers.online"
    subscriber_invite = "subscriber.invite"
    subscriber_discard = "subscriber.discard"
    connection_offer = "connection.offer"
    connection_success = "connection.success"
    connection_cancel = "connection.cancel"


class SubscriberConsumer(AsyncJsonWebsocketConsumer):
    online_subscribers_group = "subscribers"
    online_subscribers: dict[str, Literal[True]] = {}
    subscribers_offers: dict[str, str] = {}

    def get_channel_layer(self) -> InMemoryChannelLayer:
        return cast(InMemoryChannelLayer, self.channel_layer)

    def get_user(self) -> Optional[User]:
        user = cast(AnonymousUser | User, self.scope["user"])

        return cast(User, user) if getattr(user, "id", None) else None

    async def run_if_current_subscriber_is_authorized(
        self, callback: Callable[[User], Coroutine[None, None, None]]
    ) -> None:
        user = self.get_user()
        if user:
            await callback(user)

    async def connect(self) -> None:
        async def callback(user: User) -> None:
            user_id = str(user.id)

            await self.get_channel_layer().group_add(user_id, self.channel_name)
            self.online_subscribers[user_id] = True
            await self.get_channel_layer().group_send(
                self.online_subscribers_group,
                {"type": ActionType.subscriber_invite, "data": user_id},
            )

        await self.get_channel_layer().group_add(self.online_subscribers_group, self.channel_name)
        await self.run_if_current_subscriber_is_authorized(callback)
        await self.accept()

    async def disconnect(self, _: int) -> None:
        async def callback(user: User) -> None:
            user_id = str(user.id)

            await self.get_channel_layer().group_discard(user_id, self.channel_name)
            del self.online_subscribers[user_id]
            if self.subscribers_offers.get(user_id):
                del self.subscribers_offers[user_id]
            await self.get_channel_layer().group_send(
                self.online_subscribers_group,
                {"type": ActionType.subscriber_discard, "data": user_id},
            )

        await self.get_channel_layer().group_discard(
            self.online_subscribers_group,
            self.channel_name,
        )
        await self.run_if_current_subscriber_is_authorized(callback)

    async def receive_json(self, received_data: dict[str, Any]) -> None:
        match received_data.get("type", ""):
            case ActionType.subscribers_online:
                await self.handle_subscribers_online()
            case ActionType.connection_offer:
                await self.handle_connection_offer(received_data)
            case ActionType.connection_success:
                await self.handle_connection_success(received_data)
            case ActionType.connection_cancel:
                await self.handle_connection_cancel(received_data)

    # handlers
    async def handle_subscribers_online(self) -> None:
        await self.send_json(
            {"type": ActionType.subscribers_online, "data": self.online_subscribers}
        )

    async def handle_connection_offer(self, received_data: dict[str, Any]) -> None:
        async def callback(user: User) -> None:
            to_user_id = cast(str, received_data["data"])
            self.subscribers_offers[str(user.id)] = to_user_id
            await self.get_channel_layer().group_send(
                to_user_id,
                {
                    "type": ActionType.connection_offer,
                    "data": {"id": str(user.id), "full_name": user.full_name},
                },
            )

        await self.run_if_current_subscriber_is_authorized(callback)

    async def handle_connection_success(self, received_data: dict[str, Any]) -> None:
        async def callback(user: User) -> None:
            from_user_id = cast(str, received_data["data"])
            to_user_id = str(user.id)

            if self.subscribers_offers.get(from_user_id) == to_user_id:
                await self.get_channel_layer().group_send(
                    from_user_id, {"type": ActionType.connection_success}
                )
                await self.get_channel_layer().group_send(
                    to_user_id, {"type": ActionType.connection_success}
                )

        await self.run_if_current_subscriber_is_authorized(callback)

    async def handle_connection_cancel(self, received_data: dict[str, Any]) -> None:
        async def callback(user: User) -> None:
            from_user_id = cast(str, received_data["data"])
            to_user_id = str(user.id)

            if self.subscribers_offers.get(from_user_id) == to_user_id:
                await self.get_channel_layer().group_send(
                    from_user_id, {"type": ActionType.connection_cancel}
                )
                await self.get_channel_layer().group_send(
                    to_user_id, {"type": ActionType.connection_cancel}
                )

        await self.run_if_current_subscriber_is_authorized(callback)

    # group handlers
    async def subscriber_invite(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.subscriber_invite, "data": event["data"]})

    async def subscriber_discard(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.subscriber_discard, "data": event["data"]})

    async def connection_offer(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.connection_offer, "data": event["data"]})

    async def connection_success(self, _: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.connection_success})

    async def connection_cancel(self, _: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.connection_cancel})
