from typing import Self

from config.endpoint_config import EndpointConfig


class PlayerDataServiceEndpointConfig(EndpointConfig):
    def __init__(
        self,
        host: str = "localhost:3001",
        base_path: str = "players",
        api_version: str = "v0",
        app_pathname: str = "players",
    ) -> Self:
        super().__init__(host, base_path, api_version, app_pathname)