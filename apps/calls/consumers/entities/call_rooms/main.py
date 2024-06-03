import asyncio
import datetime
from typing import Any, cast

from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallRoomsStorage, CallRoomType

from .types import ActionType


class CallRoomsConsumer(AsyncConsumerHelper):
    unique_prefix = "call_rooms"
    rooms_storage = CallRoomsStorage()

    async def __wait_answerer(self, room: CallRoomType, timeout: int = 120) -> bool:
        start = datetime.datetime.now()

        while True:
            if room["is_answerer_connected"] or (datetime.datetime.now() - start).seconds > timeout:
                return room["is_answerer_connected"]

            await asyncio.sleep(0.1)

    async def __watch_limit_time(self, limit_time: int) -> None:
        start = datetime.datetime.now()

        while True:
            minutes = (datetime.datetime.now() - start).seconds // 60

            if minutes >= limit_time:
                return await self.handle_close()

            await asyncio.sleep(60)

    def get_room_id(self) -> str:
        return str(self.scope["url_route"]["kwargs"]["room_id"])

    def get_another_subscriber_channel_name(self) -> str:
        room = cast(CallRoomType, self.rooms_storage.get(self.get_room_id()))

        return self.create_unique(
            tuple(
                filter(lambda subscriber_id: str(self.subscriber.id) != subscriber_id, room["ids"])
            )[0]
        )

    async def connect(self) -> None:
        subscriber = self.get_subscriber()

        if not subscriber:
            return
        self.set_subscriber(subscriber)
        subscriber_id = str(subscriber.id)

        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)
        if (not room) or (subscriber_id not in room["ids"]):
            return

        await self.get_channel_layer().group_add(
            self.create_unique(subscriber_id), self.channel_name
        )
        await self.accept()

        (from_subscriber_id, to_subscriber_id) = room["ids"]

        match subscriber_id:
            case id if id == from_subscriber_id:
                await self.send_json({"type": ActionType.offer})
            case id if id == to_subscriber_id:
                self.rooms_storage.set_answerer_is_connected(room_id)

        for subscriber_id in room["ids"]:
            await self.send_json({"type": ActionType.time_limit, "data": room["time_limit"]})

    async def disconnect(self, _: int) -> None:
        await self.handle_close()

        await self.get_channel_layer().group_discard(
            self.create_unique(str(self.subscriber.id)), self.channel_name
        )

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        match received_content.get("type"):
            case ActionType.offer:
                await self.handle_offer(received_content)
            case ActionType.answer:
                await self.handle_answer(received_content)
            case ActionType.candidate:
                await self.handle_candidate(received_content)
            case ActionType.connected:
                await self.handle_connected()
            case ActionType.close:
                await self.handle_close()

    async def handle_offer(self, received_content: dict[str, Any]) -> None:
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        result = await self.__wait_answerer(room)
        if not result:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.answer, "data": received_content["data"]},
        )

    async def handle_answer(self, received_content: dict[str, Any]) -> None:
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.final, "data": received_content["data"]},
        )

    async def handle_candidate(self, received_content: dict[str, Any]) -> None:
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        result = await self.__wait_answerer(room)
        if not result:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.candidate, "data": received_content["data"]},
        )

    async def handle_connected(self) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)
        if (not room) or (str(self.subscriber.id) == room["ids"][1]):
            return

        self.rooms_storage.set_start(room_id)
        asyncio.create_task(self.__watch_limit_time(room["time_limit"]))

    async def handle_close(self) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)
        if not room:
            return
        self.rooms_storage.remove(room_id)

        for id in room["ids"]:
            unique_group_name = self.create_unique(id)
            await self.get_channel_layer().group_send(unique_group_name, {"type": ActionType.close})

        await self.rooms_storage.add_room_to_db(room)

    async def answer(self, received_content: dict[str, Any]) -> None:
        await self.send_json(received_content)

    async def final(self, received_content: dict[str, Any]) -> None:
        await self.send_json(received_content)

    async def candidate(self, received_content: dict[str, Any]) -> None:
        await self.send_json(received_content)

    async def close(self, _: dict[str, Any]) -> None:
        await self.send_json({"type": ActionType.close})
