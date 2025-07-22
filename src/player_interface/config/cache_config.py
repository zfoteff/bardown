from functools import lru_cache
from random import randint
from typing import Self


class CacheConfig:
    def __init__(self) -> Self:
        from os import environ

        self.host = environ["CACHE_HOST"]
        self.port = environ["CACHE_PORT"]
        self.ttl = int(environ["CACHE_TTL"]) + randint(-30, 30)
        self.read_timeout = int(environ["CACHE_TIMEOUT"])
        self.connect_timeout = int(environ["CACHE_CONNECT_TIMEOUT"])

    @property
    def url(self) -> str:
        return f"rediss://{self.host}:{self.port}"

@lru_cache()
def get_cache_config() -> CacheConfig:
    return CacheConfig()
