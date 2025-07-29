from functools import lru_cache
from typing import Self


class PlayerDataServiceConfig:
    def __init__(
        self,
        tls_enabled: bool = False,
        connect_timeout_ms: int = 500,
        read_timeout_ms: int = 500,
    ) -> Self:
        from os import environ

        self.host = environ["PLAYER_DATA_SERVICE_HOST"]
        self.tls_enabled = tls_enabled
        self.connect_timeout_ms = connect_timeout_ms
        self.read_timeout_ms = read_timeout_ms


@lru_cache()
def get_player_data_service_config() -> PlayerDataServiceConfig:
    return PlayerDataServiceConfig()
