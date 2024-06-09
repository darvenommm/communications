"""Subscriber consumer module."""

from typing import Any

from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import OnlineSubscribersStorage

from .types import ActionType


class SubscriberConsumer(AsyncConsumerHelper):
    """Subscriber Consumer.

    Args:
        AsyncConsumerHelper: async consumer Helper.
    """

    online_subscribers_group = "subscribers"
    online_subscribers_storage = OnlineSubscribersStorage()

    async def connect(self) -> None:
        """Handle subscriber connect."""
        subscriber = self.get_subscriber()

        if not subscriber:
            return

        subscriber_id = str(subscriber.id)
        self.online_subscribers_storage.add(subscriber_id)

        await self.get_channel_layer().group_add(self.online_subscribers_group, self.channel_name)
        await self.get_channel_layer().group_send(
            self.online_subscribers_group,
            {"type": ActionType.subscriber_invite, "data": subscriber_id},
        )
        await self.accept()

        await self.send_json(
            {
                "type": ActionType.subscribers_online,
                "data": self.online_subscribers_storage.get_all(),
            },
        )

    async def disconnect(self, _: int) -> None:
        """Handle subscriber disconnect.

        Args:
            _: Error code.
        """
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
        """Handle a received json.

        Args:
            received_data: Request payload.
        """
        match received_data.get("type", ""):
            case ActionType.subscribers_online:
                await self.handle_subscribers_online()

    async def handle_subscribers_online(self) -> None:
        """Handle action type: subscribers_online."""
        await self.send_json(
            {
                "type": ActionType.subscribers_online,
                "data": self.online_subscribers_storage.get_all(),
            },
        )

    async def subscriber_invite(self, event: dict[str, str]) -> None:
        """Event a channel about subscriber inviting.

        Args:
            event: Id of the invited user.
        """
        await self.send_json({"type": ActionType.subscriber_invite, "data": event["data"]})

    async def subscriber_discard(self, event: dict[str, str]) -> None:
        """Event a channel about discarding user.

        Args:
            event: id of the discarded user.
        """
        await self.send_json({"type": ActionType.subscriber_discard, "data": event["data"]})
