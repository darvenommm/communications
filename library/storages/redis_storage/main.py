"""Redis storage module."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Self

from django.core.cache import cache


class RedisStorage(ABC):
    """Abstract redis storage."""

    key: str
    __current: Optional[Self] = None

    def __new__(cls, *args, **kwargs) -> Self:
        """Create redis storage once.

        Args:
            args: Extra arguments.
            kwargs: Extra keyword arguments.

        Returns:
            Self: created redis storage entity.
        """
        if cls.__current:
            return cls.__current

        cache.set(cls.key, {}, timeout=None)
        cls.__current = super().__new__(cls, *args, **kwargs)
        return cls.__current

    @abstractmethod
    def __init__(self) -> None:
        """Init redis storage."""
        super().__init__()

    def cache_set(self, new_value: dict, timeout: Optional[int] = None) -> None:
        """Set redis cache.

        Args:
            new_value: received value.
            timeout: ttl time. Defaults to None == Infinity.
        """
        cache.set(self.key, new_value, timeout)

    @abstractmethod
    def get_all(self) -> Any:
        """Get all redis cache value.

        Returns:
            Any: the cache value.
        """
        return cache.get(self.key)

    @abstractmethod
    def add(self, *args, **kwargs) -> None:
        """Add value to the cache value.

        Args:
            args: Extra arguments.
            kwargs: Extra keyword arguments.
        """

    @abstractmethod
    def remove(self, *args, **kwargs) -> None:
        """Remove value from the cache value.

        Args:
            args: Extra arguments.
            kwargs: Extra keyword arguments.
        """
