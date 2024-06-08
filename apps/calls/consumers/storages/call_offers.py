"""Call offers storage module."""

from library.storages.redis_storage import RedisStorage


class CallOffersStorage(RedisStorage):
    """Call offers storage.

    Args:
        RedisStorage: Abstract redis storage class.
    """

    key = "subscribers-offers"

    def __init__(self) -> None:
        """Init call offers storage."""
        super().__init__()

    def get_all(self) -> dict[str, str]:
        """Get all offers.

        Returns:
            dict[str, str]: All offers. [from_subscriber_id, to_subscriber_id].
        """
        return super().get_all()

    def add(self, from_subscriber_id: str, to_subscriber_id: str) -> None:
        """Add a offer.

        Args:
            from_subscriber_id: A id of the from subscriber id.
            to_subscriber_id: A id of the to subscriber id.
        """
        offers = self.get_all()

        if offers.get(from_subscriber_id):
            return

        offers[from_subscriber_id] = to_subscriber_id
        self.cache_set(offers)

    def remove(self, from_subscriber_id: str) -> None:
        """Remove a offer.

        Args:
            from_subscriber_id: A id of the from subscriber.
        """
        offers = self.get_all()

        if not offers.get(from_subscriber_id):
            return

        offers.pop(from_subscriber_id)
        self.cache_set(offers)

    def get_other(self, from_subscriber_id: str) -> str:
        """Get other subscriber id.

        Args:
            from_subscriber_id: A id of the from subscriber.

        Raises:
            ValueError: Not found offer in the offers.

        Returns:
            str: The other subscriber id.
        """
        offers = self.get_all()
        to_subscriber_id = offers.get(from_subscriber_id)

        if not to_subscriber_id:
            raise ValueError("Not found the user in the offers!")

        return to_subscriber_id
