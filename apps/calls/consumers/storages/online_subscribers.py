from typing import Literal

from django.core.cache import cache

from library.RedisStorage import RedisStorage


class OnlineSubscribersStorage(RedisStorage):
    key = "online-subscribers"

    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> dict[str, Literal[True]]:
        return super().get_all()

    def add(self, subscriber_id: str) -> None:
        subscribers = self.get_all()

        if subscribers.get(subscriber_id):
            return

        subscribers[subscriber_id] = True
        cache.set(self.key, subscribers)

    def remove(self, subscriber_id: str) -> None:
        subscribers = self.get_all()

        if not subscribers.get(subscriber_id):
            return

        del subscribers[subscriber_id]
        cache.set(self.key, subscribers)
