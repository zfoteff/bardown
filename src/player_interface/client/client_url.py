from typing import Self

from config.player_data_service_endpoint_config import EndpointConfig


class ClientUrl:
    def __init__(self, method: str, config: EndpointConfig) -> Self:
        self.__method = method
        self.__config = config

    @property
    def method(self) -> str:
        return self.__method

    @property
    def connect_timeout_in_ms(self) -> int:
        return self.__config.connect_timeout_ms

    @property
    def url(self) -> str:
        return self.__config.compose_path()
