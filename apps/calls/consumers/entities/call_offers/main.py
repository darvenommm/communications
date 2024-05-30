from typing import Any, cast
from uuid import uuid4

from subscribers.models import Subscriber

from .types import ActionType
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallOffersStorage, CallRoomsStorage


class CallOffersConsumer(AsyncConsumerHelper):
    unique_prefix = "call_offers"
    offers_storage = CallOffersStorage()
    rooms_storage = CallRoomsStorage()

    async def connect(self) -> None:
        subscriber = self.get_subscriber()

        if not subscriber:
            return

        self.set_subscriber(subscriber)

        subscriber_group = self.create_unique(str(subscriber.id))
        await self.get_channel_layer().group_add(subscriber_group, self.channel_name)
        await self.accept()

    async def disconnect(self, _: int) -> None:
        subscriber = self.get_subscriber()

        if not subscriber:
            return

        subscriber_group = self.create_unique(str(subscriber.id))
        await self.get_channel_layer().group_discard(subscriber_group, self.channel_name)

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        match received_content.get("type", ""):
            case ActionType.offer_connection:
                await self.handle_offer_connection(received_content)
            case ActionType.offer_cancel:
                await self.handle_offer_cancel(received_content)
            case ActionType.offer_success:
                await self.handle_offer_success(received_content)

    async def handle_offer_connection(self, received_content: dict[str, str]) -> None:
        from_subscriber = self.subscriber

        from_subscriber_id = str(from_subscriber.id)
        to_subscriber_id = cast(str, received_content["data"])

        self.offers_storage.add(from_subscriber_id, to_subscriber_id)

        await self.get_channel_layer().group_send(
            self.create_unique(to_subscriber_id),
            {
                "type": ActionType.offer_connection,
                "data": {"id": from_subscriber_id, "full_name": from_subscriber.full_name},
            },
        )

    async def handle_offer_cancel(self, received_content: dict[str, str]) -> None:
        to_subscriber = self.subscriber

        from_subscriber_id = cast(str, received_content["data"])
        to_subscriber_id = str(to_subscriber.id)

        if self.offers_storage.get(from_subscriber_id) == to_subscriber_id:
            self.offers_storage.remove(from_subscriber_id)
            await self.get_channel_layer().group_send(
                self.create_unique(from_subscriber_id),
                {"type": ActionType.offer_cancel},
            )

    async def handle_offer_success(self, received_content: dict[str, Any]) -> None:
        to_subscriber = self.subscriber

        from_subscriber_id = cast(str, received_content["data"])
        to_subscriber_id = str(to_subscriber.id)

        if self.offers_storage.get(from_subscriber_id) == to_subscriber_id:
            self.offers_storage.remove(from_subscriber_id)

            call_room_id = str(uuid4())
            await self.rooms_storage.add(call_room_id, from_subscriber_id, to_subscriber_id)
            for subscriber_id in (from_subscriber_id, to_subscriber_id):
                await self.get_channel_layer().group_send(
                    self.create_unique(subscriber_id),
                    {"type": ActionType.offer_success, "data": call_room_id},
                )

    async def offer_connection(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_connection, "data": event["data"]})

    async def offer_cancel(self, _: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_cancel})

    async def offer_success(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_success, "data": event["data"]})
