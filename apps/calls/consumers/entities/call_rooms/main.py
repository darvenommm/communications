"""Call rooms consumer module."""

import asyncio
import datetime
from typing import Any, cast

from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallRoomsStorage, CallRoomType

from .types import ActionType


class CallRoomsConsumer(AsyncConsumerHelper):
    """Call Rooms Consumer."""

    unique_prefix = "call_rooms"
    rooms_storage = CallRoomsStorage()

    def get_room_id(self) -> str:
        """Get room id from url.

        Returns:
            str: room id.
        """
        return str(self.scope["url_route"]["kwargs"]["room_id"])

    def get_another_subscriber_channel_name(self) -> str:
        """Get another subscriber channel name.

        Returns:
            str: another subscriber id.
        """
        room = cast(CallRoomType, self.rooms_storage.get(self.get_room_id()))

        return self.create_unique(
            tuple(
                filter(lambda subscriber_id: str(self.subscriber.id) != subscriber_id, room["ids"]),
            )[0],
        )

    async def connect(self) -> None:
        """Handle connect."""
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
            self.create_unique(subscriber_id), self.channel_name,
        )
        await self.accept()

        (from_subscriber_id, to_subscriber_id) = room["ids"]

        match subscriber_id:
            case id_of_subscriber1 if id_of_subscriber1 == from_subscriber_id:
                await self.send_json({"type": ActionType.offer})
            case id_of_subscriber2 if id_of_subscriber2 == to_subscriber_id:
                self.rooms_storage.set_answerer_is_connected(room_id)

        for _ in room["ids"]:
            await self.send_json({"type": ActionType.time_limit, "data": room["time_limit"]})

    async def disconnect(self, _: int) -> None:
        """Handle disconnect.

        Args:
            _: Error code.
        """
        await self.handle_close()

        await self.get_channel_layer().group_discard(
            self.create_unique(str(self.subscriber.id)), self.channel_name,
        )

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        """Handle the received json.

        Args:
            received_content: Received content.
        """
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
        """Handle offer.

        Args:
            received_content: Received content.
        """
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        wait_answerer_result = await self.__wait_answerer(room)
        if not wait_answerer_result:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.answer, "data": received_content["data"]},
        )

    async def handle_answer(self, received_content: dict[str, Any]) -> None:
        """Handle answer.

        Args:
            received_content: Received data.
        """
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.final, "data": received_content["data"]},
        )

    async def handle_candidate(self, received_content: dict[str, Any]) -> None:
        """Handle candidate.

        Args:
            received_content: Received content.
        """
        room = self.rooms_storage.get(self.get_room_id())
        if not room:
            return

        wait_answerer_result = await self.__wait_answerer(room)
        if not wait_answerer_result:
            return

        await self.get_channel_layer().group_send(
            self.get_another_subscriber_channel_name(),
            {"type": ActionType.candidate, "data": received_content["data"]},
        )

    async def handle_connected(self) -> None:
        """Handle connected."""
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)
        if (not room) or (str(self.subscriber.id) == room["ids"][1]):
            return

        self.rooms_storage.set_start(room_id)
        asyncio.create_task(self.__watch_limit_time(room["time_limit"]))

    async def handle_close(self) -> None:
        """Handle close."""
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)
        if not room:
            return
        self.rooms_storage.remove(room_id)

        for subscriber_id in room["ids"]:
            unique_group_name = self.create_unique(subscriber_id)
            await self.get_channel_layer().group_send(unique_group_name, {"type": ActionType.close})

        await self.rooms_storage.add_room_to_db(room)

    async def answer(self, received_content: dict[str, Any]) -> None:
        """Event of creating answer to answerer and get offer to him.

        Args:
            received_content: Event data.
        """
        await self.send_json(received_content)

    async def final(self, received_content: dict[str, Any]) -> None:
        """Event of final stage of the RTC connection.

        Args:
            received_content: event data.
        """
        await self.send_json(received_content)

    async def candidate(self, received_content: dict[str, Any]) -> None:
        """Event of resending candidate from offerer to answerer.

        Args:
            received_content: in data candidate object.
        """
        await self.send_json(received_content)

    async def close(self, _: dict[str, Any]) -> None:
        """Send a signal of closing connection.

        Args:
            _: Event data.
        """
        await self.send_json({"type": ActionType.close})

    async def __wait_answerer(self, room: CallRoomType, timeout: int = 120) -> bool:
        """Wait answerer.

        Args:
            room: The handled room.
            timeout: Time out. Defaults to 120.

        Returns:
            bool: wait or no?
        """
        start = datetime.datetime.now()

        while True:
            if room["is_answerer_connected"] or (datetime.datetime.now() - start).seconds > timeout:
                return room["is_answerer_connected"]

            await asyncio.sleep(0.1)

    async def __watch_limit_time(self, limit_time: int) -> None:
        """Watch limit time.

        Args:
            limit_time: time limit.

        Returns:
            None: None.
        """
        start = datetime.datetime.now()

        while True:
            minutes = (datetime.datetime.now() - start).seconds // 60

            if minutes >= limit_time:
                return await self.handle_close()

            await asyncio.sleep(60)
