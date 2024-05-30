from typing import Any

from .types import ActionType
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import OnlineSubscribersStorage


class SubscriberConsumer(AsyncConsumerHelper):
    online_subscribers_group = "subscribers"
    online_subscribers_storage = OnlineSubscribersStorage()

    async def connect(self) -> None:
        subscriber = self.get_subscriber()

        if not subscriber:
            return

        subscriber_id = str(subscriber.id)
        self.online_subscribers_storage.add(subscriber_id)

        await self.get_channel_layer().group_send(
            self.online_subscribers_group,
            {"type": ActionType.subscriber_invite, "data": subscriber_id},
        )
        await self.get_channel_layer().group_add(self.online_subscribers_group, self.channel_name)
        await self.accept()

        await self.send_json(
            {
                "type": ActionType.subscribers_online,
                "data": self.online_subscribers_storage.get_all(),
            }
        )

    async def disconnect(self, _: int) -> None:
        subscriber = self.get_subscriber()

        if not subscriber:
            return

        subscriber_id = str(subscriber.id)
        self.online_subscribers_storage.remove(subscriber_id)

        await self.get_channel_layer().group_discard(
            self.online_subscribers_group,
            self.channel_name,
        )
        await self.get_channel_layer().group_send(
            self.online_subscribers_group,
            {"type": ActionType.subscriber_discard, "data": subscriber_id},
        )

    async def receive_json(self, received_data: dict[str, Any]) -> None:
        match received_data.get("type", ""):
            case ActionType.subscribers_online:
                await self.handle_subscribers_online()

    async def handle_subscribers_online(self) -> None:
        await self.send_json(
            {
                "type": ActionType.subscribers_online,
                "data": self.online_subscribers_storage.get_all(),
            }
        )

    async def subscriber_invite(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.subscriber_invite, "data": event["data"]})

    async def subscriber_discard(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.subscriber_discard, "data": event["data"]})
