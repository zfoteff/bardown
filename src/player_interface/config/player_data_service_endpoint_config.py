from typing import Self

from config.endpoint_config import EndpointConfig


class PlayerDataServiceEndpointConfig(EndpointConfig):
    def __init__(self) -> Self:
        super().__init__(
            base_url="http://127.0.0.1:3001",
            base_path="/",
            api_version="v0",
            app_pathname="players",
        )

    def compose_path(self) -> str:
        """
        Create base path for all requests based on environment configuration
        """
        return f"{self.base_url}/{self.app_pathname}/{self.api_version}/"
