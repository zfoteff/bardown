from random import randint
from typing import Self, Dict


class CacheConfig:
    _config: Dict[str, str] = {}

    def __init__(self, config: Dict[str, str]) -> Self:
        self._config = config
        self._host = self._config["CACHE_HOST"]
        self._port = self._config["CACHE_PORT"]
        self._ttl = self._config["CACHE_TTL"]
        self._read_timeout = self._config["CACHE_TIMEOUT"]
        self._connect_timeout = self._config["CACHE_CONNECT_TIMEOUT"]

    @property
    def url(self) -> str:
        return f"rediss://{self.host}:{self.port}"

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return int(self._port)
    
    @property
    def connect_timeout(self) -> int:
        return int(self._connect_timeout)

    @property
    def ttl(self) -> int:
        """Add [-30, 30] second modifier to key ttl

        Returns:
            int: Cache entry TTL [-30, 30] second modifier applied
        """
        modifier = randint(-30, 30)
        return int(self._ttl) + modifier
