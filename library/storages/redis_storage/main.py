from abc import ABC, abstractmethod
from typing import Any, Self, Optional

from django.core.cache import cache


class RedisStorage(ABC):
    key: str
    __current: Optional[Self] = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__current:
            return cls.__current

        cache.set(cls.key, {})
        cls.__current = super().__new__(cls, *args, **kwargs)
        return cls.__current

    def cache_set(self, new_value: Any, timeout: Optional[int] = None) -> None:
        cache.set(self.key, new_value, timeout)

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_all(self) -> Any:
        return cache.get(self.key)

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    def remove(self, *args, **kwargs) -> None:
        pass
