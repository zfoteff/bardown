from typing import Self

from config.player_data_service_endpoint_config import PlayerDataServiceConfig


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
        """
        Create base path for all requests based on environment configuration
        """
        protocol = "https://" if self._tls_enabled else "http://"
        return f"{protocol}{self.__config.host}/{self.__path}"
    
    @property
    def connect_timeout_in_ms(self) -> int:
        return self.__config.connect_timeout_ms

    @property
    def url(self) -> str:
        return self.__config.compose_path()
