"""Online subscribers storage module."""
from typing import Literal

from library.storages.redis_storage import RedisStorage


class OnlineSubscribersStorage(RedisStorage):
    """Storage of online subscribers.

    Args:
        RedisStorage: Abstract redis storage class.
    """

    key = "online-subscribers"

    def __init__(self) -> None:
        """Init a subscribers storage."""
        super().__init__()

    def get_all(self) -> dict[str, Literal[True]]:
        """Get all subscriber.

        Returns:
            dict[str, Literal[True]]: Subscriber with True values. Always True.
        """
        return super().get_all()

    def add(self, subscriber_id: str) -> None:
        """Add a subscriber.

        Args:
            subscriber_id: A id of the subscriber.
        """
        online_subscribers = self.get_all()

        if online_subscribers.get(subscriber_id):
            return

        online_subscribers[subscriber_id] = True
        self.cache_set(online_subscribers)

    def remove(self, subscriber_id: str) -> None:
        """Remove a subscriber.

        Args:
            subscriber_id: A id of the subscriber.
        """
        online_subscribers = self.get_all()

        if not online_subscribers.get(subscriber_id):
            return

        online_subscribers.pop(subscriber_id)
        self.cache_set(online_subscribers)
