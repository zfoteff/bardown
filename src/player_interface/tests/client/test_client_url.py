from client.client_url import ClientUrl
from config.player_data_service_config import PlayerDataServiceConfig
from tests.bin.decorators.timed import timed

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_valid_endpoint_config() -> None:
    config = PlayerDataServiceConfig("123")
    config2 = PlayerDataServiceConfig()
    config2.host = "456"
    assert config.host == "123"
    assert config2.host == "456"


@timed(logger)
def test_create_valid_client_url_with_empty_config() -> None:
    config = PlayerDataServiceConfig()
    url = ClientUrl("/path", "GET", config)
    assert url.path == "/path"
    assert url.method == "GET"
