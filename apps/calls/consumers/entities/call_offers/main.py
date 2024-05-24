from typing import Any, cast
from uuid import uuid4

from .types import ActionType
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallOffersStorage, CallRoomsStorage


class CallOffersConsumer(AsyncConsumerHelper):
    user_unique_prefix = "call_offers"
    offers_storage = CallOffersStorage()
    rooms_storage = CallRoomsStorage()

    async def connect(self) -> None:
        try:
            user = self.get_user()
        except ValueError:
            return

        user_group = self.create_unique_group(str(user.id))
        await self.get_channel_layer().group_add(user_group, self.channel_name)
        await self.accept()

    async def disconnect(self, _: int) -> None:
        user = self.get_user()
        user_group = self.create_unique_group(str(user.id))
        await self.get_channel_layer().group_discard(user_group, self.channel_name)

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        match received_content.get("type", ""):
            case ActionType.offer_connection:
                await self.handle_offer_connection(received_content)
            case ActionType.offer_cancel:
                await self.handle_offer_cancel(received_content)
            case ActionType.offer_success:
                await self.handle_offer_success(received_content)

    async def handle_offer_connection(self, received_content: dict[str, str]) -> None:
        from_user = self.get_user()

        from_user_id = str(from_user.id)
        to_user_id = cast(str, received_content["data"])

        self.offers_storage.add(from_user_id, to_user_id)

        await self.get_channel_layer().group_send(
            self.create_unique_group(to_user_id),
            {
                "type": ActionType.offer_connection,
                "data": {"id": from_user_id, "full_name": from_user.full_name},
            },
        )

    async def handle_offer_cancel(self, received_content: dict[str, str]) -> None:
        to_user = self.get_user()

        from_user_id = cast(str, received_content["data"])
        to_user_id = str(to_user.id)

        if self.offers_storage.get(from_user_id) == to_user_id:
            self.offers_storage.remove(from_user_id)
            await self.get_channel_layer().group_send(
                self.create_unique_group(from_user_id),
                {"type": ActionType.offer_cancel},
            )

    async def handle_offer_success(self, received_content: dict[str, Any]) -> None:
        to_user = self.get_user()

        from_user_id = cast(str, received_content["data"])
        to_user_id = str(to_user.id)

        if self.offers_storage.get(from_user_id) == to_user_id:
            self.offers_storage.remove(from_user_id)

            call_room_id = str(uuid4())
            self.rooms_storage.add(call_room_id, from_user_id, to_user_id)
            for user_id in (from_user_id, to_user_id):
                await self.get_channel_layer().group_send(
                    self.create_unique_group(user_id),
                    {"type": ActionType.offer_success, "data": call_room_id},
                )

    async def offer_connection(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_connection, "data": event["data"]})

    async def offer_cancel(self, _: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_cancel})

    async def offer_success(self, event: dict[str, str]) -> None:
        await self.send_json({"type": ActionType.offer_success, "data": event["data"]})
