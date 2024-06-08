"""Call rooms storage module."""

import asyncio
import datetime
from typing import Optional, Required, TypedDict, cast
from uuid import uuid4

from calls.models import Operator, SubscriberCall
from django.db import models
from django.utils import timezone
from subscribers.models import Subscriber

from library.storages.redis_storage import RedisStorage


class CallRoomType(TypedDict):
    """Call Room Type."""

    ids: Required[tuple[str, str]]
    start_time: Required[Optional[datetime.datetime]]
    is_answerer_connected: Required[bool]
    time_limit: Required[int]  # in minutes


class CallRoomsStorage(RedisStorage):
    """Call room storage.

    Args:
        RedisStorage: Abstract redis storage class.
    """

    key = "call-rooms"

    def __init__(self) -> None:
        """Init call rooms storage."""
        super().__init__()

    def get_all(self) -> dict[str, CallRoomType]:
        """Get rooms.

        Returns:
            dict[str, CallRoomType]: The gotten rooms.
        """
        return super().get_all()

    def get(self, room_id: str) -> Optional[CallRoomType]:
        """Get room.

        Args:
            room_id: A id of the room.

        Returns:
            Optional[CallRoomType]: The gotten room.
        """
        return self.get_all().get(room_id)

    async def add(self, from_subscriber_id: str, to_subscriber_id: str) -> str:
        """Add room.

        Args:
            from_subscriber_id: A id of the from subscriber.
            to_subscriber_id: A id of the to subscriber.

        Returns:
            str: A id of the created room.
        """
        rooms = self.get_all()
        room_id = str(uuid4())

        async with asyncio.TaskGroup() as tg:
            from_subscriber_task = tg.create_task(Subscriber.objects.aget(id=from_subscriber_id))
            to_subscriber_task = tg.create_task(Subscriber.objects.aget(id=to_subscriber_id))

        from_subscriber_operators = cast(
            models.QuerySet[Operator], getattr(await from_subscriber_task, "operators"),
        ).all()
        to_subscriber_operators = cast(
            models.QuerySet[Operator], getattr(await to_subscriber_task, "operators"),
        ).all()

        time_limit = 10
        async for from_operator in from_subscriber_operators:
            async for to_operator in to_subscriber_operators:
                if from_operator.id == to_operator.id:
                    time_limit = 15

        rooms[room_id] = {
            "ids": (from_subscriber_id, to_subscriber_id),
            "start_time": None,
            "is_answerer_connected": False,
            "time_limit": time_limit,
        }

        self.cache_set(rooms)

        return room_id

    def remove(self, room_id: str) -> None:
        """Remove room.

        Args:
            room_id: A id of the room.
        """
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms.pop(room_id)
        self.cache_set(rooms)

    def set_answerer_is_connected(self, room_id: str) -> None:
        """Set answerer is connected.

        Args:
            room_id: A id of the room.
        """
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["is_answerer_connected"] = True
        self.cache_set(rooms)

    def set_start(self, room_id: str) -> None:
        """Set start of the room.

        Args:
            room_id: A id of the room.
        """
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["start_time"] = timezone.now()
        self.cache_set(rooms)

    async def add_room_to_db(self, room: CallRoomType) -> None:
        """Add a room to the django db.

        Args:
            room: room data for adding to the db.
        """
        (from_subscriber_id, to_subscriber_id) = room["ids"]

        async with asyncio.TaskGroup() as tg:
            from_subscriber_task = tg.create_task(Subscriber.objects.aget(id=from_subscriber_id))
            to_subscriber_task = tg.create_task(Subscriber.objects.aget(id=to_subscriber_id))

            from_subscriber = await from_subscriber_task
            to_subscriber = await to_subscriber_task

        duration = timezone.now() - cast(datetime.datetime, room["start_time"])
        await SubscriberCall.objects.acreate(
            caller=from_subscriber,
            receiver=to_subscriber,
            start=room["start_time"],
            duration=duration,
        )
