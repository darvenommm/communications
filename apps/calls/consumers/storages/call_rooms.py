import asyncio
from typing import cast, TypedDict, Required, Optional
import datetime

from subscribers.models import Subscriber
from calls.models import SubscriberCall
from library.storages.redis_storage import RedisStorage


class CallRoomType(TypedDict):
    ids: Required[tuple[str, str]]
    start_time: Required[Optional[datetime.datetime]]
    is_answerer_connected: Required[bool]


class CallRoomsStorage(RedisStorage):
    key = "call-rooms"

    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> dict[str, CallRoomType]:
        return super().get_all()

    def get(self, room_id: str) -> Optional[CallRoomType]:
        return self.get_all().get(room_id)

    def add(self, room_id: str, from_subscriber_id: str, to_subscriber_id: str) -> None:
        rooms = self.get_all()

        if rooms.get(room_id):
            return

        rooms[room_id] = {
            "ids": (from_subscriber_id, to_subscriber_id),
            "start_time": None,
            "is_answerer_connected": False,
        }

        self.cache_set(rooms)

    def remove(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        del rooms[room_id]
        self.cache_set(rooms)

    def set_answerer_is_connected(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["is_answerer_connected"] = True
        self.cache_set(rooms)

    def set_start(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["start_time"] = datetime.datetime.now()
        self.cache_set(rooms)

    async def add_room_to_db(self, room: CallRoomType) -> None:
        (from_subscriber_id, to_subscriber_id) = room["ids"]

        async with asyncio.TaskGroup() as tg:
            from_subscriber_task = tg.create_task(Subscriber.objects.aget(id=from_subscriber_id))
            to_subscriber_task = tg.create_task(Subscriber.objects.aget(id=to_subscriber_id))

            from_subscriber = await from_subscriber_task
            to_subscriber = await to_subscriber_task

        duration = datetime.datetime.now() - cast(datetime.datetime, room["start_time"])
        await SubscriberCall.objects.acreate(
            caller=from_subscriber,
            receiver=to_subscriber,
            start=room["start_time"],
            duration=duration,
        )
