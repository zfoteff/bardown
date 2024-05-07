from config.endpoint_config import EndpointConfig


class PlayerDataServiceEndpointConfig(EndpointConfig):
    def __init__(self) -> None:
        super().__init__(
            base_url="127.0.0.1:3001", 
            base_path="/", 
            api_version="v0", 
            app_pathname=""
        )
