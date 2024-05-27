from django.core.cache import cache

from library.RedisStorage import RedisStorage


class CallOffersStorage(RedisStorage):
    key = "subscribers-offers"

    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> dict[str, str]:
        return super().get_all()

    def add(self, from_subscriber_id: str, to_subscriber_id: str) -> None:
        offers = self.get_all()

        if offers.get(from_subscriber_id):
            return

        offers[from_subscriber_id] = to_subscriber_id
        self.cache_set(offers)

    def remove(self, from_subscriber_id: str) -> None:
        offers = self.get_all()

        if not offers.get(from_subscriber_id):
            return

        del offers[from_subscriber_id]
        self.cache_set(offers)

    def get(self, from_subscriber_id: str) -> str:
        offers = self.get_all()
        to_subscriber_id = offers.get(from_subscriber_id)

        if not to_subscriber_id:
            raise ValueError("Not found the user in the offers!")

        return to_subscriber_id
