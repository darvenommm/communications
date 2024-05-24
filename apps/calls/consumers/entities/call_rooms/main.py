from typing import Any, cast

from .types import ActionType
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallRoomsStorage


class CallRoomsConsumer(AsyncConsumerHelper):
    user_unique_prefix = "call_rooms"
    rooms_storage = CallRoomsStorage()

    def get_room_id(self) -> str:
        return str(self.scope["url_route"]["kwargs"]["room_id"])

    async def connect(self) -> None:
        try:
            user_id = str(self.get_user().id)
        except ValueError:
            return

        room = self.rooms_storage.get(self.get_room_id())

        if (not room) or (user_id not in room.get("ids", [])):
            return

        user_group_name = self.create_unique_group(user_id)
        await self.get_channel_layer().group_add(user_group_name, self.channel_name)
        await self.accept()

        (from_user_id, to_user_id) = cast(list[str], room["ids"])

        if user_id == from_user_id:
            await self.send_json({"type": ActionType.offer_create})

        if user_id == to_user_id and room["offer"]:
            await self.get_channel_layer().group_send(
                self.create_unique_group(to_user_id),
                {"type": ActionType.offer_send, "data": room["offer"]},
            )

    async def disconnect(self, _: int) -> None:
        self.rooms_storage.remove(self.get_room_id())

        user_id = str(self.get_user().id)
        await self.get_channel_layer().group_discard(
            self.create_unique_group(user_id), self.channel_name
        )

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        match received_content.get("type"):
            case ActionType.offer_send:
                await self.handle_offer_send(received_content)
            case ActionType.answer_send:
                await self.handler_answer_send(received_content)

    async def handle_offer_send(self, received_content: dict[str, Any]) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        if not room:
            return

        to_user_id = cast(list[str], room.get("ids"))[1]
        self.rooms_storage.set_offer(room_id, received_content["data"])

        await self.get_channel_layer().group_send(
            self.create_unique_group(to_user_id),
            received_content,
        )

    async def handler_answer_send(self, received_content: dict[str, Any]) -> None:
        room = self.rooms_storage.get(self.get_room_id())

        if not room:
            return

        from_user_id = cast(list[str], room.get("ids"))[0]
        await self.get_channel_layer().group_send(
            self.create_unique_group(from_user_id),
            received_content,
        )

    async def offer_send(self, received_content: dict[str, Any]) -> None:
        await self.send_json({"type": ActionType.answer_create, "data": received_content["data"]})

    async def answer_send(self, received_content: dict[str, Any]) -> None:
        await self.send_json({"type": ActionType.answer_get, "data": received_content["data"]})
