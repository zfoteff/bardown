from random import randint
from typing import Self


class CacheConfig:
    def __init__(self) -> Self:
        self._host = "localhost"
        self._port = 6379
        self._ttl = 300  # Cache ttl in seconds. Default: 5 minutes

    @property
    def url(self) -> str:
        return f"rediss://{self._host}:{self._port}"

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def ttl(self) -> int:
        """Add [-30, 30] second modifier to key ttl

        Returns:
            int: Cache entry TTL [-30, 30] second modifier applied
        """
        modifier = randint(-30, 30)
        return self._ttl + modifier
