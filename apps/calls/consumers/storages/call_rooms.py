from typing import Any
import datetime

from django.core.cache import cache
from library.RedisStorage import RedisStorage


class CallRoomsStorage(RedisStorage):
    key = "call-rooms"

    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> dict[str, Any]:
        return super().get_all()

    def get(self, room_id: str) -> dict | None:
        return self.get_all().get(room_id)

    def add(self, room_id: str, from_subscriber_id: str, to_subscriber_id: str) -> None:
        rooms = self.get_all()

        if rooms.get(room_id):
            return

        rooms[room_id] = {
            "ids": [from_subscriber_id, to_subscriber_id],
            "start_time": None,
            from_subscriber_id: None,
            to_subscriber_id: None,
        }

        cache.set(self.key, rooms)

    def remove(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        del rooms[room_id]
        cache.set(self.key, rooms)

    def set_start(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["start_time"] = str(datetime.datetime.now())
        cache.set(self.key, rooms)

    def set_subscriber_offer(self, room_id: str, subscriber_id: str, offer: dict) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id][subscriber_id] = offer
        cache.set(self.key, rooms)
