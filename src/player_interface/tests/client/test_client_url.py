from client.client_url import ClientURL
from config.endpoint_config import EndpointConfig
from config.player_data_service_endpoint_config import PlayerDataServiceEndpointConfig
from tests.bin.decorators.timed import timed

from bin.logger import Logger

logger = Logger("test")


@timed(logger)
def test_valid_endpoint_config() -> None:
    config = EndpointConfig("123")
    config2 = PlayerDataServiceEndpointConfig()
    config2.base_url = "456"
    assert config.base_url == "123"
    assert config2.base_url == "456"


@timed(logger)
def test_create_valid_client_url_with_required_fields() -> None:
    url = ClientURL("/path", "GET")
    assert url.path == "/path"
    assert url.method == "GET"
    assert url.path_parameters is None
    assert url.query_parameters is None


@timed(logger)
def test_create_valid_client_url_with_optional_fields() -> None:
    path_params = ["e98cf157-d1cf-42fd-9dd4-39aa9979d864"]
    query_params = {"filter.number": 6, "filter.position": "Attack"}
    url = ClientURL("/path", "GET", path_params, query_params)
    assert url.path == "path"
    assert url.method == "GET"
    assert "e98cf157-d1cf-42fd-9dd4-39aa9979d864" in url.path_parameters
    assert (
        "filter.number" in url.query_parameters.keys()
        and "filter.position" in url.query_parameters.keys()
    )
