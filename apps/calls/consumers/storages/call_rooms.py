from typing import Any, cast, TypedDict, Required, NotRequired, Optional
import datetime

from django.core.cache import cache
from library.storages.redis_storage import RedisStorage


class CallRoomType(TypedDict):
    ids: Required[tuple[str, str]]
    candidates: Required[dict[str, list[str]]]
    start_time: Required[Optional[datetime.datetime]]
    offer: Required[Optional[dict[str, Any]]]
    answer: Required[Optional[dict[str, Any]]]


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
            "offer": None,
            "answer": None,
            "candidates": {
                from_subscriber_id: [],
                to_subscriber_id: [],
            },
        }

        self.cache_set(rooms)

    def remove(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        del rooms[room_id]
        self.cache_set(rooms)

    def set_start(self, room_id: str) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["start_time"] = datetime.datetime.now()
        self.cache_set(rooms)

    def set_offer(self, room_id: str, offer: dict) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["offer"] = offer
        self.cache_set(rooms)

    def set_answer(self, room_id: str, answer: dict) -> None:
        rooms = self.get_all()

        if not rooms.get(room_id):
            return

        rooms[room_id]["answer"] = answer
        cache.set(self.key, rooms)

    def add_candidate(self, room_id: str, to: str, candidate: dict) -> None:
        rooms = self.get_all()
        room = rooms.get(room_id)

        if not room or (to not in room["ids"]):
            return

        cast(list, rooms[room_id]["candidates"][to]).append(candidate)
        self.cache_set(rooms)

    def get_candidates(self, room_id: str, to: str) -> list[dict]:
        rooms = self.get_all()
        room = rooms.get(room_id)

        if not room or (to not in room["ids"]):
            return []

        candidates = cast(list, rooms[room_id]["candidates"][to]).copy()
        rooms[room_id]["candidates"][to] = []

        self.cache_set(rooms)

        return candidates
