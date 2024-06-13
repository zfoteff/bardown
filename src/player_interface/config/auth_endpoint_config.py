from typing import Self

from config.endpoint_config import EndpointConfig


class AuthEndpointConfig(EndpointConfig):
    def __init__(
        self,
        base_url: str = "http://0.0.0.0:3001",
        base_path: str = "/",
        api_version: str = "v0",
        app_pathname: str = "auth",
    ) -> Self:
        super().__init__(base_url, base_path, api_version, app_pathname)
