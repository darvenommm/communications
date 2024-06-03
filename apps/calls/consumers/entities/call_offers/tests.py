import asyncio
from django.test import TestCase
from channels.testing import WebsocketCommunicator

from subscribers.models import Subscriber
from .main import CallOffersConsumer
from .types import ActionType


class MyTests(TestCase):
    async def test_success(self):
        communicator1 = WebsocketCommunicator(CallOffersConsumer.as_asgi(), "/call-offers/")
        communicator2 = WebsocketCommunicator(CallOffersConsumer.as_asgi(), "/call-offers/")

        subscriber1 = Subscriber(username="test", first_name="name", last_name="surname")
        subscriber1.set_password("password")
        await subscriber1.asave()

        subscriber2 = Subscriber(username="test2", first_name="name", last_name="surname")
        subscriber2.set_password("password")
        await subscriber2.asave()

        communicator1.scope["user"] = subscriber1
        communicator2.scope["user"] = subscriber2

        async with asyncio.TaskGroup() as tg:
            connection_task1 = tg.create_task(communicator1.connect())
            connection_task2 = tg.create_task(communicator2.connect())

        connected1, _ = await connection_task1
        connected2, _ = await connection_task2

        assert connected1 and connected2

        await communicator1.send_json_to(
            {"type": ActionType.offer_connection, "data": str(subscriber2.id)}
        )

        await communicator2.receive_json_from()
        await communicator2.send_json_to(
            {"type": ActionType.offer_success, "data": str(subscriber1.id)}
        )

        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_cancel(self) -> None:
        communicator1 = WebsocketCommunicator(CallOffersConsumer.as_asgi(), "/call-offers/")
        communicator2 = WebsocketCommunicator(CallOffersConsumer.as_asgi(), "/call-offers/")

        subscriber1 = Subscriber(username="test", first_name="name", last_name="surname")
        subscriber1.set_password("password")
        await subscriber1.asave()

        subscriber2 = Subscriber(username="test2", first_name="name", last_name="surname")
        subscriber2.set_password("password")
        await subscriber2.asave()

        communicator1.scope["user"] = subscriber1
        communicator2.scope["user"] = subscriber2

        async with asyncio.TaskGroup() as tg:
            connection_task1 = tg.create_task(communicator1.connect())
            connection_task2 = tg.create_task(communicator2.connect())

        connected1, _ = await connection_task1
        connected2, _ = await connection_task2

        assert connected1 and connected2

        await communicator1.send_json_to(
            {"type": ActionType.offer_connection, "data": str(subscriber2.id)}
        )

        await communicator2.receive_json_from()
        await communicator2.send_json_to(
            {"type": ActionType.offer_cancel, "data": str(subscriber1.id)}
        )

        await communicator1.disconnect()
        await communicator2.disconnect()
