from typing import Any, cast

from .types import ActionType
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallRoomsStorage


class CallRoomsConsumer(AsyncConsumerHelper):
    rooms_storage = CallRoomsStorage()

    def get_room_id(self) -> str:
        return str(self.scope["url_route"]["kwargs"]["room_id"])

    async def connect(self) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        user_id = str(self.get_user().id)

        if (not room) or (user_id not in room.get("ids", [])):
            return

        await self.get_channel_layer().group_add(room_id, self.channel_name)
        await self.accept()

        from_user_id = cast(list, room["ids"])[0]

        if user_id == from_user_id:
            await self.send_json({"type": ActionType.offer})

    async def disconnect(self, _: int) -> None:
        room_id = self.get_room_id()

        self.rooms_storage.remove(room_id)
        await self.get_channel_layer().group_discard(room_id, self.channel_name)

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        pass
