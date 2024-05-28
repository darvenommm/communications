from typing import Any, cast

from .types import ActionType, WhoAmI
from calls.consumers.helpers import AsyncConsumerHelper
from calls.consumers.storages import CallRoomsStorage


class CallRoomsConsumer(AsyncConsumerHelper):
    unique_prefix = "call_rooms"
    rooms_storage = CallRoomsStorage()

    def get_room_id(self) -> str:
        return str(self.scope["url_route"]["kwargs"]["room_id"])

    async def connect(self) -> None:
        try:
            subscriber_id = str(self.get_subscriber().id)
        except ValueError:
            return

        room = self.rooms_storage.get(self.get_room_id())
        if (not room) or (subscriber_id not in room.get("ids", [])):
            return

        await self.accept()

        from_subscriber_id = cast(list[str], room["ids"])[0]
        await self.send_json(
            {
                "type": ActionType.who,
                "data": WhoAmI.starter if subscriber_id == from_subscriber_id else WhoAmI.answerer,
            }
        )

    async def disconnect(self, _: int) -> None:
        self.rooms_storage.remove(self.get_room_id())

    async def receive_json(self, received_content: dict[str, Any]) -> None:
        match received_content.get("type"):
            case ActionType.offer_send:
                await self.handle_offer_send(received_content)
            case ActionType.answer_send:
                await self.handle_answer_send(received_content)
            case ActionType.candidate_send:
                await self.handle_candidate_send(received_content)
            case ActionType.offer_get:
                await self.handle_offer_get()
            case ActionType.answer_get:
                await self.handle_answer_get()
            case ActionType.candidate_get:
                await self.handle_candidate_get()

    async def handle_offer_send(self, received_content: dict[str, Any]) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        if not room:
            return

        self.rooms_storage.set_offer(room_id, received_content["data"])

    async def handle_answer_send(self, received_content: dict[str, Any]) -> None:
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        if not room:
            return

        self.rooms_storage.set_answer(room_id, received_content["data"])

    async def handle_offer_get(self) -> None:
        room = self.rooms_storage.get(self.get_room_id())

        if not room:
            return

        await self.send_json({"type": ActionType.offer_get, "data": room["offer"]})

    async def handle_answer_get(self) -> None:
        room = self.rooms_storage.get(self.get_room_id())

        if not room:
            return

        await self.send_json({"type": ActionType.answer_get, "data": room["answer"]})

    async def handle_candidate_send(self, received_content: dict[str, Any]) -> None:
        subscriber = self.get_subscriber()
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        if not room:
            return

        need_subscriber_id = list(
            filter(lambda subscriber_id: subscriber_id != str(subscriber.id), room["ids"])
        )[0]
        self.rooms_storage.add_candidate(room_id, need_subscriber_id, received_content["data"])

    async def handle_candidate_get(self) -> None:
        subscriber_id = str(self.get_subscriber().id)
        room_id = self.get_room_id()
        room = self.rooms_storage.get(room_id)

        if not room:
            return

        candidates = self.rooms_storage.get_candidates(room_id, subscriber_id)

        await self.send_json({"type": ActionType.candidate_get, "data": candidates})
