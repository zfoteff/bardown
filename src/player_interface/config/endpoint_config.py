from random import randint
from typing import Self

class PlayerDataServiceConfig:
    def __init__(
        self,
        host: str = "",
        base_path: str = "",
        api_version: str = "",
        app_pathname: str = "",
        tls_enabled: bool = False,
        connect_timeout_ms: int = 500,
        read_timeout_ms: int = 500,
    ) -> None:
        from os import environ

        self.host = environ["PLAYER_DATA_SERVICE_HOST"]
        self.base_path = base_path
        self.api_version = api_version
        self.app_pathname = app_pathname
        self.tls_enabled = tls_enabled
        self.connect_timeout_ms = connect_timeout_ms
        self.read_timeout_ms = read_timeout_ms


    @property
    def path(self) -> str:
        """
        Create base path for all requests based on environment configuration
        """
        protocol = "https://" if self._tls_enabled else "http://"
        return (
            f"{protocol}{self.host}/{self.base_path}/{self.api_version}/{self.app_pathname}"
            if self.app_pathname is not None
            else f"{protocol}{self.host}/{self.base_path}/{self.api_version}/"
        )