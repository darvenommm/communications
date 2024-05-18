from abc import ABC, abstractmethod
from typing import Any, Self

from django.core.cache import cache


class RedisStorage(ABC):
    key: str
    __current: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__current:
            return cls.__current

        cache.set(cls.key, {})
        cls.__current = super().__new__(cls, *args, **kwargs)
        return cls.__current

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    def get_all(self) -> Any:
        return cache.get(self.key)

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def remove(self, *args, **kwargs) -> None:
        pass
