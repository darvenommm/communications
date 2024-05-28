from typing import Literal

from library.storages.redis_storage import RedisStorage


class OnlineSubscribersStorage(RedisStorage):
    key = "online-subscribers"

    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> dict[str, Literal[True]]:
        return super().get_all()

    def add(self, subscriber_id: str) -> None:
        online_subscribers = self.get_all()

        if online_subscribers.get(subscriber_id):
            return

        online_subscribers[subscriber_id] = True
        self.cache_set(online_subscribers)

    def remove(self, subscriber_id: str) -> None:
        online_subscribers = self.get_all()

        if not online_subscribers.get(subscriber_id):
            return

        del online_subscribers[subscriber_id]
        self.cache_set(online_subscribers)
