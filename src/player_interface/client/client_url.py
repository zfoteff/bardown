from typing import Self

from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig


class ClientUrl:
    def __init__(
        self,
        path: str,
        method: str,
    ) -> Self:
        self.__path = path
        self.__method = method
        self.__config = PlayerDataServiceEndpointConfig()

    @property
    def path(self) -> str:
        return self.__path

    @property
    def method(self) -> str:
        return self.__method

    @property
    def connect_timeout_in_ms(self) -> int:
        return self.__config.connect_timeout_ms

    @property
    def url(self) -> str:
        return self.__config.compose_path() + self.__path
