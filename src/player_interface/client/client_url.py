from typing import Self

from config.player_data_service_config import PlayerDataServiceConfig


class ClientUrl:
    def __init__(self, method: str, path: str, config: PlayerDataServiceConfig) -> Self:
        self.__method = method
        self.__config = config
        self.__path = path

    @property
    def method(self) -> str:
        return self.__method

    @property
    def path(self) -> str:
        return self.__path

    @property
    def url(self) -> str:
        return f"{"https://" if self.__config.tls_enabled else "http://"}{self.__config.host}/{self.__path}"

    @property
    def connect_timeout_in_ms(self) -> int:
        return self.__config.connect_timeout_ms

    @property
    def read_timeout_in_ms(self) -> int:
        return self.__config.read_timeout_ms
