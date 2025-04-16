from typing import Self

from config.endpoint_config import EndpointConfig


class PlayerDataServiceEndpointConfig(EndpointConfig):
    def __init__(
        self,
        base_url: str = "http://localhost:3001",
        base_path: str = "players",
        api_version: str = "v0",
        app_pathname: str = "players",
    ) -> Self:
        super().__init__(base_url, base_path, api_version, app_pathname)

    # def __init__(self, config: EndpointConfig, base_path, api_version) -> Self:
    #     super().__init__(config.base_url, base_path, api_version, config.app_pathname)
