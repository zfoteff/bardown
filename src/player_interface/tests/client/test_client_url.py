__version__ = "1.0.0"
__author__ = "Zac Foteff"

from bin.logger import Logger
from config.endpoint_config import EndpointConfig
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from tests.bin.decorators.timed import timed

logger = Logger("test")


@timed(logger)
def test_valid_endpoint_config() -> None:
    config = EndpointConfig("123")
    config2 = PlayerDataServiceEndpointConfig()
    config2.base_url = "456"
    assert config.base_url == "123"
    assert config2.base_url == "456"
