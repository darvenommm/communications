"""Subscriber consumer test case."""
import asyncio

from channels.testing import WebsocketCommunicator
from django.test import TestCase
from subscribers.models import Subscriber

from .main import SubscriberConsumer
from .types import ActionType


class SubscriberConsumerTestCase(TestCase):
    """Subscriber consumer test case."""

    async def test_success(self):
        """Test success connection."""
        subscriber1 = Subscriber(username="test", first_name="name", last_name="surname")
        subscriber1.set_password("password")
        await subscriber1.asave()

        subscriber2 = Subscriber(username="test2", first_name="name", last_name="surname")
        subscriber2.set_password("password")
        await subscriber2.asave()

        communicator1 = WebsocketCommunicator(SubscriberConsumer.as_asgi(), "/subscribers/")
        communicator2 = WebsocketCommunicator(SubscriberConsumer.as_asgi(), "/subscribers/")

        communicator1.scope["user"] = subscriber1
        communicator2.scope["user"] = subscriber2

        async with asyncio.TaskGroup() as tg:
            connection_task1 = tg.create_task(communicator1.connect())
            connection_task2 = tg.create_task(communicator2.connect())

        connected1, _ = await connection_task1
        connected2, _ = await connection_task2

        assert connected1 and connected2

        await communicator1.send_json_to({"type": ActionType.subscribers_online})

        response = await communicator1.receive_json_from()
        assert len(response["data"].items()) == 2

        await communicator1.disconnect()
        await communicator2.disconnect()
